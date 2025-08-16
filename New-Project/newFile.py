import pandas as pd
from flask import Flask, render_template, request, jsonify
from fantasyPros import fantasyProsDF
from SleeperWithESPN import sleeperESPNDF
from ffaRankings import FFA_combined_df
import webbrowser
import threading
import time

# -----------------------------------------------------------------------------------------------------------------------------------
# What to do next year:
# Should just be able to use global dataframes to have it scrape again. Shouldn't have to retouch this file.



# Initialize Flask app
app = Flask(__name__)

# -----------------------------------------------------------------------------------------------------------------------------------

# Sample ADP data (mimicking scraped data structure)
initial_data = {
    'Player': ['Blank'],
    'Position': ['RB'],
    'ADP': [1.2],
    'Team': ['SF']
}

# Create global DataFrames
adp_df_sleeperESPN = sleeperESPNDF if not sleeperESPNDF.empty else pd.DataFrame(initial_data)
adp_df_fantasyPros = fantasyProsDF if not fantasyProsDF.empty else pd.DataFrame(initial_data)


# Merge the two DataFrames into a single DataFrame
adp_df_merged = pd.merge(adp_df_fantasyPros, adp_df_sleeperESPN, on='Player', how='left')
adp_df_merged = pd.merge(adp_df_merged, FFA_combined_df, on='Player', how='left')

# Fill NaN values in ADP columns with 0
adp_df_merged['FFA_Rank'] = adp_df_merged['FFA_Rank'].fillna(0)
adp_df_merged['FFA_Rank'] = adp_df_merged['FFA_Rank'].astype(int)

# drop null values in ADP columns
adp_df_merged = adp_df_merged.dropna(subset=['ADP_FP', 'ADP_Sleeper', 'ADP_ESPN'])
adp_df_merged = adp_df_merged.reset_index(drop=True)
initial_df = adp_df_merged.copy()

# -----------------------------------------------------------------------------------------------------------------------------------

def create_table_html(df):
    # Purpose: This function creates an HTML table from a DataFrame with remove buttons for each player.
    # Parameters:
    # df (pd.DataFrame): The DataFrame containing player data.
    # Returns:
    # str: HTML string representing the table with remove buttons.
    
    """Create HTML table with remove buttons"""
    if df.empty:
        return "<p style='text-align: center; font-style: italic;'>No players found for the selected filter.</p>"
    
    html = '<table id="adpTable" class="display adp-table" style="width:100%;">'
    html += '''
    <thead>
        <tr>
            <th>Player</th>
            <th>Team</th>
            <th>Position</th>
            <th>ADP_ESPN</th>
            <th>ADP_Sleeper</th>
            <th>ADP_FP</th>
            <th>PosRank_ESPN</th>
            <th>PosRank_Sleeper</th>
            <th>PosRank_FP</th>
            <th>PosRank_FFA</th>
            <th>Action</th>
        </tr>
    </thead>
    <tbody>
    '''
    for _, row in df.iterrows():
        html += f'''
        <tr>
            <td>{row["Player"]}</td>
            <td>{row["Team"]}</td>
            <td>{row["Position"]}</td>
            <td>{row["ADP_ESPN"]}</td>
            <td>{row["ADP_Sleeper"]}</td>
            <td>{row["ADP_FP"]}</td>
            <td>{row["ESPN_POSRANK"]}</td>
            <td>{row["Sleeper_POSRANK"]}</td>
            <td>{row["FP_POSRANK"]}</td>
            <td>{row["FFA_Rank"]}</td>
            <td><button class="remove-btn" data-player="{row["Player"]}">Remove</button></td>
        </tr>
        '''

    html += '</tbody></table>'
    return html

@app.route('/')
def display_adp_board():
    # Purpose: This route displays the ADP board with an optional position filter.
    # Parameters: None
    # Returns: Rendered HTML template with the ADP board and position filter.

    global adp_df_merged
    
    # Get position filter from query parameters
    position_filter = request.args.get('position', '')

    # print the position filter for debugging
    print(f"Position filter: {position_filter}")
    
    # Filter DataFrame if position is specified
    if position_filter != 'All' and position_filter != '':
        filtered_df = adp_df_merged[adp_df_merged['Position'] == position_filter]
    elif position_filter == 'All':
        filtered_df = adp_df_merged[adp_df_merged['Position'].isin(['QB', 'RB', 'WR', 'TE'])]
    elif position_filter == '':
        filtered_df = adp_df_merged

    # Sort by ADP
    filtered_df = filtered_df.sort_values(by='ADP')
    
    # Create table HTML
    table_html = create_table_html(filtered_df)
    
    # Use render_template instead of render_template_string
    return render_template('index.html', table=table_html, position_filter=position_filter)


@app.route('/remove_player', methods=['POST'])
def remove_player():
    # Purpose: This route handles the removal of a player from the ADP DataFrame.
    # Parameters: None
    # Returns: JSON response indicating success or failure of the operation.

    global adp_df_merged

    print("Received request to remove player")
    
    try:
        data = request.get_json()
        player_name = data.get('player')
        
        if player_name:
            # Remove the player from the DataFrame
            print(f"Removing player: {player_name}")
            adp_df_merged = adp_df_merged[adp_df_merged['Player'] != player_name]
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'No player name provided'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/reset_data', methods=['POST'])
def reset_data():
    # Purpose: This route resets the ADP DataFrame to its initial state.
    # Parameters: None
    # Returns: JSON response indicating success or failure of the operation.

    global adp_df_merged
    
    try:
        # Reset to initial data
        adp_df_merged = initial_df if not adp_df_merged.empty else pd.DataFrame(initial_data)
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Function to open the browser
def open_browser():
    # Purpose: This function opens the default web browser to the Flask app URL.
    # Parameters: None
    # Returns: None

    time.sleep(1)  # Wait for Flask server to start
    webbrowser.open('http://127.0.0.1:5000')

# -----------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    # Start Flask server in a separate thread
    #threading.Thread(target=open_browser).start()
    threading.Thread(target=open_browser).start()
    app.run(debug=True, use_reloader=False)  # Changed to debug=True as requested