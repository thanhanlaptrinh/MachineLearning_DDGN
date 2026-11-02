"""Kiểm tra phần hoàn thiện: nguồn nhãn, ngưỡng, dữ liệu chương 3 và trạng thái API."""
import sys,json
from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'service'),str(ROOT/'notebooks_or_src_py')]
from audit_engine import AuditEngine,fit_assessment,sha,RATE
from flexible_engine import FlexibleEngine
from training_report import build_training_report

def main():
 checks=[]
 def check(name,ok):
  assert ok,name
  checks.append({'check':name,'passed':True})
 e=AuditEngine();f=FlexibleEngine(e);before={p:sha(ROOT/p) for p in e.report['source_files']}
 for ratio,gap,label in [(2.60,.0768,'Khoảng cách lớn'),(1.77,.0641,'Khoảng cách vừa'),(2.72,.0908,'Khoảng cách lớn'),(2.42,.179,'Khoảng cách lớn'),(1.33,.0336,'Khoảng cách nhỏ'),(1.1,.01,'Chưa thấy dấu hiệu rõ'),(1.2,.10,'Khoảng cách lớn'),(1.2,.06,'Khoảng cách vừa'),(1.2,.03,'Khoảng cách nhỏ')]:
  a=fit_assessment({'mae':1.,'r2':.99},{'mae':ratio,'r2':.99-gap},e.report['baseline']);check(f'Overfit {ratio} {gap}',a['label']==label and 'tham khảo' in a['detail'])
 for scope,ids,counts,color in [('train_only',e.train_ids[:30],{'train':30},'red'),('holdout_only',e.test_ids[:30],{'holdout':30},'green'),('mixed',e.train_ids[:15]+e.test_ids[:15],{'train':15,'holdout':15},'red')]:
  q=f.evaluate({'records':[{'source_id':i} for i in ids]})
  check(scope+' scope and banner',q['evaluation_scope']==scope and q['banner_color']==color)
  for m in q['models']:
   check(scope+' '+m['id']+' membership counts',{g:v['n'] for g,v in m['by_membership'].items()}==counts)
   check(scope+' '+m['id']+' headline count',m['metrics']['n']==counts[q['headline_membership']])
  if scope=='train_only':a=q
  if scope=='holdout_only':b=q
 check('XGB lower error on training sample',next(m for m in a['models'] if m['id']=='xgboost')['metrics']['mae']<next(m for m in b['models'] if m['id']=='xgboost')['metrics']['mae'])
 for slug in e.models:
  q=f.evaluate({'records':[{'source_id':e.test_ids[0]}],'models':[slug],'explain':True})
  check(slug+' single sample has no R2',q['models'][0]['metrics']['r2'] is None)
  check(slug+' trace verified',q['models'][0]['trace']['verified'])
 q=f.evaluate({'records':[{'features':{'GrLivArea':1500,'OverallQual':6},'actual_vnd':5e9}],'models':['boosting']})
 check('Unknown labels are unverified',q['evaluation_scope']=='unverified_only' and q['banner_color']=='yellow' and q['rows'][0]['truth']=='user_supplied')
 r=build_training_report(e)
 for m in r['models']:
  check(m['id']+' actual top15',len(m['important_features'])==15)
  check(m['id']+' feature display removes prefix',all(not v['feature'].startswith(('num__','cat__')) for v in m['important_features']))
  check(m['id']+' tuning and saved variant agree',m['target_transform']==m['tuning']['selected']['variant'])
 eda=json.loads((ROOT/'results/eda_report.json').read_text());df=pd.read_csv(ROOT/'data/train.csv')
 check('Chapter3 raw stats from train.csv',eda['price_stats_usd']['mean']==df.SalePrice.mean() and eda['price_stats_usd']['skew']==df.SalePrice.skew())
 check('Chapter3 all 1460 rows kept',eda['removed_rows']==0 and len(e.X_train)+len(e.X_test)==len(df))
 check('79 inputs (36 numeric,43 categorical), no Id',eda['feature_count']==len(f.columns)==79 and eda['numeric_count']==36 and eda['categorical_count']==43 and 'Id' not in f.columns)
 for scope,ids,filename in [('train',e.train_ids,'du_doan_TRAIN_chi_tiet.csv'),('test',e.test_ids,'du_doan_TEST_chi_tiet.csv')]:
  table=pd.read_csv(ROOT/'results/chuan_hoa'/filename,float_precision='round_trip')
  for slug,_,_ in __import__('audit_engine').CATALOG:
   part=table[table.Mo_hinh==next(m['name'] for m in r['models'] if m['id']==slug)]
   X=e.X_train if scope=='train' else e.X_test
   check(slug+' '+scope+' CSV matches model',np.allclose(part.Du_doan_VND,np.asarray(e.models[slug].predict(X),float)*RATE,rtol=0,atol=.01))
 check('No protected artifacts mutated',all(sha(ROOT/p)==v for p,v in before.items()))
 save={'status':'PASS','passed':len(checks),'failed':0,'checks':checks}
 (ROOT/'results/verification_completion.json').write_text(json.dumps(save,ensure_ascii=False,indent=2))
 print('PASS',len(checks),'completion checks')
if __name__=='__main__':main()
