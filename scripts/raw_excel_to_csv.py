
# https://youtu.be/9tC7-jY6ZJk?t=407

valid_groups = [1,2,4,6,8] 

x = '''396.2	1.8
414	1.7
336.6	1.1
322.6	1.4
393.6	1.4
448.2	1.9
451.8	1.7
453	1.8
449.4	1.5
453.8	1.5
449.4	1.2
478.2	1.1
401.6	1.1
438.6	1.5
401.8	1.7
421.4	2.1
452.6	1.7
468.2	1.4
402.4	1.1
399.8	1.6
397.6	1.6
415	1.3
417	1.5
372.6	1.1
399.2	1.7
381.2	1.6
391.8	1.9
413.4	1.8
425	1.6
478.8	2.2
439.8	1.5
400	1.1
437.6	1.3
402.6	1.3
412.6	1.3
441.8	1.1
398.8	1.1
420.4	1.6
419.6	1.8
366.4	1.3
442	1.6
421	1
375.8	1.6
429.6	1.4
419.6	1.2
379.4	1.1
398.4	2.1
430	1.9
430	1.3
417	1.7'''

# x = '\n'.join([val for ix,val in enumerate(x.split('\n')) if any(10*group_id <= ix < 10*(group_id+1) for group_id in valid_groups) ])

y = '''6	4	5	4	1	1	2	6
7	6	6	5	3	2	3	5
6	3	4	4	4	2	1	6
6	2	4	6	6	0	0	4
5	5	3	6	5	3	3	3
7	6	6	5	6	0	0	6
5	4	3	4	3	0	0	3
2	4	2	4	5	5	0	5
3	3	6	8	4	1	1	4
3	5	7	4	2	1	2	5
8	10	10	8	5	4	3	3
7	8	7	10	8	6	5	4
6	8	8	9	5	5	5	3
7	7	8	11	7	4	8	4
5	9	7	8	8	5	6	6
7	9	11	7	9	4	5	2
9	10	8	7	8	3	4	2
10	9	9	10	8	5	4	4
8	4	5	5	6	4	6	3
8	7	3	4	7	6	5	5
1	2	5	5	4	0	0	4
4	4	8	4	2	4	1	3
5	3	7	7	3	3	0	5
4	7	2	6	2	5	2	5
3	5	6	8	4	1	1	5
5	3	8	6	4	2	1	8
4	8	4	2	5	2	2	7
6	4	6	3	6	3	1	8
3	8	4	3	2	2	3	8
4	9	7	5	1	1	4	4
8	9	9	9	5	8	2	5
9	7	6	10	7	9	5	2
5	5	7	9	7	6	1	3
5	8	8	8	3	9	4	2
2	6	7	4	6	2	5	4
1	3	4	7	2	8	5	6
7	2	5	6	1	3	6	8
2	4	7	9	5	6	5	4
7	8	9	8	2	6	2	6
8	5	9	6	4	3	3	2
8	8	6	5	8	1	1	11
9	7	5	3	7	3	3	10
4	7	7	5	7	3	4	9
4	7	3	9	5	3	2	3
8	6	6	7	5	3	2	7
3	4	4	5	5	3	2	5
5	3	8	7	7	3	3	6
7	5	5	6	8	2	5	4
6	3	8	8	3	2	4	9
7	7	6	8	3	3	2	5'''




import numpy as np
import pandas as pd

df_o = pd.read_csv('data/proc/behavior_04week.csv')

label_cols = ['nAChR','BDNF','Trk-β','BDNF','BDNF','IL-6','iNOS','Nrf-2']

# Applicable to Behavioral Dataset
# df_n = pd.DataFrame([ list(map(float,f'{i}\t{j}'.split())) for i,j in zip(x.split('\n'), y.split('\n')) ])
# df_n.columns = ['body_wt','brain_wt'] + label_cols
# for col in ['group_id','cgrt_cnt','nctn_mg','dose_mg']:
#     df_n[col] = df_o[col]

# Applicable to Gene expression data
df_n = pd.DataFrame([ j.split() for j in y.split('\n') ])
df_n.columns = label_cols

aux_arr = np.concatenate([[df_o[df_o['group_id']==group_id].loc[:,['cgrt_cnt','nctn_mg','dose_mg']].iloc[0].to_list()]*10 for group_id in valid_groups], axis=0).T.astype(int)
df_n['group_id'] = [ group_id for group_id in valid_groups for ix in range(10) ]
df_n['cgrt_cnt'] = aux_arr[0] ; df_n['nctn_mg'] = aux_arr[1] ; df_n['dose_mg'] = aux_arr[2]

for col in label_cols:
    df_n[col] = df_n[col].astype(int)


# df_n[['group_id','body_wt','brain_wt','cgrt_cnt','nctn_mg','dose_mg','hypalg_bfr','hypalg_aft']].to_csv('data/behavior_12week.csv',index=False, header=True)

df_n[['group_id','cgrt_cnt', 'nctn_mg','dose_mg','nAChR','BDNF','Trk-β','BDNF','BDNF','IL-6','iNOS','Nrf-2']].to_csv('data/genetic_12week.csv',index=False, header=True)
