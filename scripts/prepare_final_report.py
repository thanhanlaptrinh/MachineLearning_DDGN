"""Sinh số liệu báo cáo và quy trình từ dữ liệu, báo cáo CV và trọng số đã lưu; không fit."""
import sys,json,platform,hashlib,importlib.metadata
from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'service'),str(ROOT/'notebooks_or_src_py')]
from audit_engine import AuditEngine,RATE,CATALOG,sha
from training_report import build_training_report

def save(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
def main():
 e=AuditEngine();report=build_training_report(e);out=ROOT/'results/chuan_hoa';out.mkdir(exist_ok=True)
 df=e.df;test=pd.read_csv(ROOT/'data/test.csv');features=df.drop(columns=['SalePrice','Id']);num=features.select_dtypes('number');cat=features.select_dtypes('object')
 stats={k:float(v) for k,v in df.SalePrice.describe().items()};stats['skew']=float(df.SalePrice.skew());stats['kurtosis']=float(df.SalePrice.kurt())
 missing=df.isna().sum().sort_values(ascending=False);corr=df.select_dtypes('number').corr()['SalePrice'].drop(['SalePrice','Id']).sort_values(ascending=False)
 eda={'train_shape':list(df.shape),'test_shape':list(test.shape),'feature_count':len(features.columns),'numeric_count':len(num.columns),'categorical_count':len(cat.columns),'duplicate_rows':int(df.duplicated().sum()),'missing_cells':int(df.isna().sum().sum()),'missing_columns':int((missing>0).sum()),'missing':[{'feature':k,'count':int(v),'percent':float(v/len(df)*100)} for k,v in missing.items() if v>0],'price_stats_usd':stats,'price_stats_million_vnd':{k:(v if k in ['count','skew','kurtosis'] else v*RATE/1e6) for k,v in stats.items()},'correlation':[{'feature':k,'pearson':float(v)} for k,v in corr.items()], 'outliers_grlivarea_gt4000_price_lt300000':[int(v) for v in df.loc[(df.GrLivArea>4000)&(df.SalePrice<300000),'Id']], 'quality_1_2':[{'Id':int(row.Id),'quality':int(row.OverallQual),'price_usd':float(row.SalePrice)} for _,row in df[df.OverallQual<=2].iterrows()], 'highest_prices':[{'Id':int(row.Id),'price_usd':float(row.SalePrice)} for _,row in df.nlargest(3,'SalePrice').iterrows()], 'removed_rows':0,'data_sha256':{p:sha(ROOT/p) for p in ['data/train.csv','data/test.csv']}}
 save(ROOT/'results/eda_report.json',eda)
 for scope,filename,X,y,ids in [('train','TRAIN',e.X_train,e.y_train,e.train_ids),('test','TEST',e.X_test,e.y_test,e.test_ids)]:
  rows=[];details=[]
  for m in report['models']:
   score=m['metrics'][scope];rows.append({'Mo_hinh':m['name'],**score})
   pred=np.asarray(e.models[m['id']].predict(X),float)*RATE
   for i,a,p in zip(ids,np.asarray(y,float)*RATE,pred):details.append({'Mo_hinh':m['name'],'Id':int(i),'Thuc_te_VND':float(a),'Du_doan_VND':float(p),'Sai_so_VND':float(p-a),'APE_percent':float(abs(p-a)/a*100)})
  pd.DataFrame(rows).to_csv(out/f'ket_qua_{filename}.csv',index=False,encoding='utf-8-sig');pd.DataFrame(details).to_csv(out/f'du_doan_{filename}_chi_tiet.csv',index=False,encoding='utf-8-sig')
 tuning=json.loads((ROOT/'results/tuning_report.json').read_text());manifest=json.loads((ROOT/'models/final/manifest.json').read_text())
 cv=[]
 for slug,m in tuning['models'].items():cv.append({'Mo_hinh':m['name'],'CV_truoc_USD':m['original_with_Id_cv']['mae'],'CV_doi_chung_bo_Id_USD':m['original_without_Id_cv']['mae'],'CV_sau_USD':m['selected']['cv_mae'],'CV_sau_VND':m['selected']['cv_mae']*RATE,'CV_std_USD':m['selected']['cv_std'],'Bien_doi_gia':m['selected']['variant'],**{f'Fold_{i+1}_USD':v for i,v in enumerate(m['selected']['fold_mae'])}})
 pd.DataFrame(cv).to_csv(out/'CV_truoc_sau.csv',index=False,encoding='utf-8-sig')
 versions={p:importlib.metadata.version(p) for p in ['scikit-learn','xgboost','pandas','numpy','scipy','joblib','Flask']};versions['python']=platform.python_version()
 steps=[('Dữ liệu','data/train.csv, data/test.csv','results/eda_report.json',f'{len(df)} dòng có nhãn, {len(test)} dòng không nhãn','Dữ liệu gốc được bảo toàn bằng SHA-256.'),('Khảo sát','data/train.csv','results/figures/, eda_report.json',f'{len(features.columns)} đặc trưng; {len(num.columns)} số, {len(cat.columns)} phân loại','Khảo sát giá, giá trị thiếu, tương quan và ngoại lệ; không loại dòng.'),('Tiền xử lý','notebooks_or_src_py/preprocess.py','Pipeline trong models/final/',f'{len(features.columns)} cột đầu vào, không có Id','Điền trung vị cho số; nhãn Missing và mã hóa một nóng cho phân loại; fit trong mỗi fold.'),('Chia dữ liệu','data/train.csv','results/tuning_selection.json',f'{len(e.X_train)} train / {len(e.X_test)} holdout; seed 42','Giữ nguyên cách chia 80/20 của nhóm.'),('Huấn luyện và tinh chỉnh','tune_models.py, tập train','results/tuning_report.json, tuning_cv_results/',f'{len(tuning["models"])} mô hình; CV {tuning["cv"]["folds"]} phần','Cây quyết định tìm lưới; ba mô hình tổ hợp tìm ngẫu nhiên raw/log. Hồi quy tuyến tính là đối chứng.'),('Chọn mô hình','results/tuning_selection.json','models/final/manifest.json',f'Mô hình thắng CV: {report["winner"]}','Chọn MAE CV thấp nhất; hòa dùng độ lệch chuẩn CV nhỏ hơn. Không chọn lại theo holdout.'),('Đánh giá','models/final/, holdout cố định','results/training_holdout_report.json',f'{len(e.X_test)} căn holdout; có cả chỉ số train','Suy luận lại để kiểm chứng số liệu đã lưu; chưa phải kiểm nghiệm ngoài Ames.'),('Chạy ứng dụng','service/predict_service.py, server.js','Giao diện tại cổng 3000',f'{len(report["models"])} mô hình dùng chung ở các trang','Nhập dữ liệu, so sánh giá và chỉ số, tách nhóm train/holdout/chưa xác minh.')]
 process={'versions':versions,'rate':RATE,'source_model_manifest_sha256':sha(ROOT/'models/final/manifest.json'),'selection_rule':tuning['selection_rule'],'winner':report['winner'],'steps':[dict(name=n,input=i,output=o,summary=s,description=d) for n,i,o,s,d in steps]}
 save(ROOT/'results/pipeline_manifest.json',process);pd.DataFrame(process['steps']).to_csv(ROOT/'results/pipeline_manifest.csv',index=False,encoding='utf-8-sig')
 save(ROOT/'results/training_holdout_report.json',report)
 # Actual datasets for the two membership demonstrations.
 for name,ids in [('train_30',e.train_ids[:30]),('holdout_30',e.test_ids[:30])]:
  frame=df[df.Id.isin(ids)].set_index('Id').loc[ids].reset_index();frame['ActualPriceVND']=frame.pop('SalePrice')*RATE;frame.to_csv(ROOT/'public/examples'/f'{name}.csv',index=False,encoding='utf-8-sig')
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 figs=ROOT/'results/figures';figs.mkdir(exist_ok=True)
 fig,ax=plt.subplots(figsize=(7,4));ax.hist(df.SalePrice,bins=40,color='#16766a');ax.set(xlabel='SalePrice (USD)',ylabel='Count');fig.tight_layout();fig.savefig(figs/'hinh_3_3_phan_phoi_gia.png',dpi=150);plt.close(fig)
 c=df[list(corr.head(9).index)+['SalePrice']].corr();fig,ax=plt.subplots(figsize=(8,6));im=ax.imshow(c,vmin=-1,vmax=1,cmap='coolwarm');ax.set_xticks(range(len(c)),c.columns,rotation=70,ha='right');ax.set_yticks(range(len(c)),c.columns);fig.colorbar(im,ax=ax);fig.tight_layout();fig.savefig(figs/'hinh_3_4_tuong_quan.png',dpi=150);plt.close(fig)
 for no,key in [('3_5','GrLivArea'),('3_6','OverallQual')]:
  fig,ax=plt.subplots(figsize=(7,4));ax.scatter(df[key],df.SalePrice,s=12,alpha=.5);ax.set(xlabel=key+(' (sqft)' if key=='GrLivArea' else ''),ylabel='SalePrice (USD)');fig.tight_layout();fig.savefig(figs/f'hinh_{no}.png',dpi=150);plt.close(fig)
 print('Generated EDA, current TRAIN/TEST, CV tables, process manifest and figures from actual code.')
if __name__=='__main__':main()
