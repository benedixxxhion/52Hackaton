import repeat as rp
import pandas as pd

P_BESS_1 = [12000, 7500, 3000, 4500, -18000, -7500, -1500, 9000, 19500, 20000, 20000, 20000, 11500, 0, 0, 0, 0, 0, 0, -20000, -20000, -20000, -20000, -20000]
P_BESS_2 = P_BESS_1[1:] + P_BESS_1[:1]
P_RES_1 = [18000, 16500, 15000, 13500, 12000, 12000, 13500, 15000, 16500, 18000, 19500, 21000, 22500, 24000, 25500, 27000, 28500, 30000, 28500, 27000, 25500, 24000, 22500, 21000]
P_RES_2 = P_RES_1[1:] + P_RES_1[:1]
P_LOAD = [60000, 54000, 48000, 48000, 54000, 60000, 72000, 84000, 96000, 102000, 108000, 114000, 120000, 114000, 108000, 102000, 108000, 120000, 114000, 96000, 84000, 72000, 66000, 60000]
R1 = [380*380/load for load in P_LOAD]
R2 = R1[1:] + R1[:1]

def Model():
    apiKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjQwNzA5OTUxOTksImlhdCI6MTc2MTE1MTg1NCwidXNlcklkIjoyMTMyfQ.Ut996TmGeaC3UVe2PMSj7U1kt3y3RP_CBln2zI3cAjw'
    user = rp.User(token=apiKey)
    app = rp.Application(user)

    projectId = 125966
    t_interval = rp.TimeInterval(start=1, end=10000) 
    model = app.get_exploration_model(projectId, t_interval)

    for i in range(24):
        variables = pd.Series({'SW': 5,
                        'P_BESS_1': P_BESS_1[i],
                        'P_BESS_2': P_BESS_2[i],
                        'P_RES_1': P_RES_1[i],
                        'P_RES_2': P_RES_2[i],
                        'R1': R1[i],
                        'R2': R2[i]}, dtype = float)

        with model as md:
            md.run(variables)
            result1 = md.get_results("U_OUT_SG") 
            result2 = md.get_results("P_OUT_LOAD")
            print('Расчет ', i+1)
            print(result1.tail())
            print(result2.tail()) 

            result1_df = result1.reset_index()
            result1_df.columns = ['Время, с', 'U_OUT_SG']
            result1_df['Время, с'] = result1_df['Время, с'] / 1000 

            result2_df = result2.reset_index()
            result2_df.columns = ['Время, с', 'P_OUT_LOAD']
            result2_df['Время, с'] = result2_df['Время, с'] / 1000

            result1_df.to_csv(f"52_U_OUT_SG_h{i}-h{i+1}.csv", sep = ';', index=False, decimal = ',')
            result2_df.to_csv(f"52_P_OUT_LOAD_h{i}-h{i+1}.csv", sep = ';', index=False, decimal = ',')

Model()
print('Расчет окончен')
    