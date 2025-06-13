from espn import df
from QBS.evaluationQBs import merged_qbs_df
from RBS.evaluationRBs import merged_rbs_df
from WRS.evaluationWRs import merged_wrs_df
from TES.evaluationTEs import merged_tes_df
import pandas as pd

# Get the postition rankings for each position
filtered_wr_df = df[df['Position'] == 'WR']
filtered_wr_df = filtered_wr_df.reset_index(drop=True)

filtered_wr_df.index = filtered_wr_df.index + 1
filtered_wr_df['ESPN Rk'] = filtered_wr_df.index

filtered_rb_df = df[df['Position'] == 'RB']
filtered_rb_df = filtered_rb_df.reset_index(drop=True)

filtered_rb_df.index = filtered_rb_df.index + 1
filtered_rb_df['ESPN Rk'] = filtered_rb_df.index

filtered_qb_df = df[df['Position'] == 'QB']
filtered_qb_df = filtered_qb_df.reset_index(drop=True)

filtered_qb_df.index = filtered_qb_df.index + 1
filtered_qb_df['ESPN Rk'] = filtered_qb_df.index

filtered_te_df = df[df['Position'] == 'TE']
filtered_te_df = filtered_te_df.reset_index(drop=True)

filtered_te_df.index = filtered_te_df.index + 1
filtered_te_df['ESPN Rk'] = filtered_te_df.index

# Merge dfs
merged_tes_df = pd.merge(merged_tes_df, filtered_te_df, on='Name', how='left')
merged_rbs_df = pd.merge(merged_rbs_df, filtered_rb_df, on='Name', how='left')
merged_wrs_df = pd.merge(merged_wrs_df, filtered_wr_df, on='Name', how='left')
merged_qbs_df = pd.merge(merged_qbs_df, filtered_qb_df, on='Name', how='left')

# Merge in youtube df for RB
youtube_rb_df = pd.read_csv('Youtube Data/YoutubeRB.csv')
merged_rbs_df = pd.merge(merged_rbs_df, youtube_rb_df, on='Name', how='left')
merged_rbs_df['BDGE Rk'] = merged_rbs_df['BDGE Rk'].fillna(1000)
merged_rbs_df['Flock Rk'] = merged_rbs_df['Flock Rk'].fillna(1000)

# Merge in youtube df for WR
youtube_wr_df = pd.read_csv('Youtube Data/YoutubeWR.csv')
merged_wrs_df = pd.merge(merged_wrs_df, youtube_wr_df, on='Name', how='left')
merged_wrs_df['BDGE Rk'] = merged_wrs_df['BDGE Rk'].fillna(1000)
merged_wrs_df['Flock Rk'] = merged_wrs_df['Flock Rk'].fillna(1000)

merged_wrs_df['ESPN Rk'] = merged_wrs_df['ESPN Rk'].fillna(1000)
merged_wrs_df = merged_wrs_df.astype({
    'ESPN Rk': 'int',
    'Rk': 'int',
    'BDGE Rk': 'int',
    'Flock Rk': 'int',
    'UnderDog Rk': 'int',
    'Sleeper Rk': 'int'
})

merged_qbs_df['ESPN Rk'] = merged_qbs_df['ESPN Rk'].fillna(1000)
merged_qbs_df['BDGE Rk'] = 1000
merged_qbs_df['Flock Rk'] = 1000
merged_qbs_df = merged_qbs_df.astype({
    'ESPN Rk': 'int',
    'Rk': 'int',
    'UnderDog Rk': 'int',
    'Sleeper Rk': 'int'
})

merged_tes_df['BDGE Rk'] = 1000
merged_tes_df['Flock Rk'] = 1000
merged_tes_df = merged_tes_df.astype({
    'ESPN Rk': 'int',
    'Rk': 'int',
    'UnderDog Rk': 'int',
    'Sleeper Rk': 'int'
})

merged_rbs_df['ESPN Rk'] = merged_rbs_df['ESPN Rk'].fillna(1000)
merged_rbs_df = merged_rbs_df.astype({
    'ESPN Rk': 'int',
    'BDGE Rk': 'int',
    'Flock Rk': 'int',
    'Rk': 'int',
    'UnderDog Rk': 'int',
    'Sleeper Rk': 'int'
})


# Finalize the cols
merged_tes_df = merged_tes_df[[ 'Name', 'Last_Rankings', 'Sleeper Rk', 'BDGE Rk', 'Flock Rk', 'ESPN Rk', 'Rk', 'UnderDog Rk', 'Last_PTS/P/G', 'PTS/P/G']]
merged_rbs_df = merged_rbs_df[[ 'Name', 'Last_Rankings', 'Sleeper Rk', 'BDGE Rk', 'Flock Rk', 'ESPN Rk', 'Rk', 'UnderDog Rk', 'Last_PTS/P/G', 'PTS/P/G']]
merged_wrs_df = merged_wrs_df[[ 'Name', 'Last_Rankings', 'Sleeper Rk', 'BDGE Rk', 'Flock Rk', 'ESPN Rk', 'Rk', 'UnderDog Rk', 'Last_PTS/P/G', 'PTS/P/G']]
merged_qbs_df = merged_qbs_df[[ 'Name', 'Last_Rankings', 'Sleeper Rk', 'BDGE Rk', 'Flock Rk', 'ESPN Rk', 'Rk', 'UnderDog Rk', 'Last_PTS/P/G', 'PTS/P/G']]