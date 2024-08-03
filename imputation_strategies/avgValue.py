import os
import numpy as np
import pandas as pd
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner


def impute(data: pd.DataFrame = None) -> pd.DataFrame:
    if data is None:
        return "fill values with an avg velocity to connect two disconnected segments"
    
    assert all(col in data.columns for col in ['time', 'X#wcentroid', 'Y#wcentroid']), f"Expected columns of ['time', 'X#wcentroid', 'Y#wcentroid']\nRecieved: {[col for col in data.columns]}"
    
    dataCleaner = TRexDataCleaner()
    
    data.reset_index(drop=True)
    
    lastValidIndex = 0
    
    for f in range(1, len(data)):
        
        if data['X#wcentroid'][f] in ('infinity', np.inf): 
            i = f
            while(data['X#wcentroid'][i] in ('infinity', np.inf)):
                i = i + 1
                continue
            nextValidIndex = i
            print(f"\nLastValidRow: \n ({data['X#wcentroid'][lastValidIndex]}, {data['Y#wcentroid'][lastValidIndex]}) \nNextValidRow: \n ({data['X#wcentroid'][nextValidIndex]}, {data['Y#wcentroid'][nextValidIndex]})")

            velocityX = getVelocity(data.loc[lastValidIndex, 'X#wcentroid'], data.loc[nextValidIndex, 'X#wcentroid'], data.loc[lastValidIndex, 'time'], data.loc[nextValidIndex, 'time'])
            velocityY = getVelocity(data.loc[lastValidIndex, 'Y#wcentroid'], data.loc[nextValidIndex, 'Y#wcentroid'], data.loc[lastValidIndex, 'time'], data.loc[nextValidIndex, 'time'])
            print("\nVelocityX: ", velocityX, "VelocityY: ", velocityY, "dtime: ", data.loc[nextValidIndex, 'time'], "-", data.loc[lastValidIndex, 'time'], "=", data.loc[nextValidIndex, 'time']-data.loc[lastValidIndex, 'time'])
            for imputeIndex in range(lastValidIndex + 1, nextValidIndex):
                data.loc[imputeIndex, 'X#wcentroid'] = data.loc[nextValidIndex, 'X#wcentroid'] + velocityX * (imputeIndex - lastValidIndex)
                data.loc[imputeIndex, 'Y#wcentroid'] = data.loc[nextValidIndex, 'Y#wcentroid'] + velocityY * (imputeIndex - lastValidIndex)
                print(f"Imputing: ({(data.loc[imputeIndex, 'X#wcentroid'])}, {data.loc[imputeIndex, 'Y#wcentroid']})")
        else:
            lastValidIndex = f
        
    return data
    
def getVelocity(pi, pf, ti, tf) -> float:
    return (pf - pi)/(tf-ti)
    