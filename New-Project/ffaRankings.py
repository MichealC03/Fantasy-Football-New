import pandas as pd

# read from csv file
FFA_rb_df =pd.read_csv('ffa_RB.csv')
print(FFA_rb_df.head())

FFA_rb_df = FFA_rb_df.fillna(1000)

FFA_rb_df['FFA_Rank'] = FFA_rb_df['FFA_Rank'].astype(int)

# same thing for WR
FFA_wr_df = pd.read_csv('ffa_WR.csv')

FFA_wr_df = FFA_wr_df.fillna(1000)
FFA_wr_df['FFA_Rank'] = FFA_wr_df['FFA_Rank'].astype(int)
print(FFA_wr_df.head())

#combine the two DataFrames into a single DataFrame
FFA_combined_df = pd.concat([FFA_rb_df, FFA_wr_df], ignore_index=True)