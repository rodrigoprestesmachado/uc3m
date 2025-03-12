import pandas as pd

def generate_detailed_diagram_with_correct_numbering(input_csv_path, output_puml_path):
    """
    Generates a state diagram in .puml format with correct numbering and
    time conversion to hours when greater than 60 minutes.

    Rules:
    - Blocks and transitions are numbered sequentially.
    - Time is converted to hours when greater than 60 minutes.
    - Spacings and interleavings are represented by arrows (-->)
      with details.

    Args:
    - input_csv_path: Path to the CSV file.
    - output_puml_path: Path to save the generated .puml file.
    """
    # Load the CSV
    data = pd.read_csv(input_csv_path, sep=';')

    # Filter interactions performed by the user
    user_interactions = data[data['Role'] == 'User'].copy()

    # Convert columns to the correct formats
    user_interactions['Datetime'] = pd.to_datetime(
        user_interactions['Datetime'], format='%H:%M:%S - %d/%m/%Y', errors='coerce')
    user_interactions = user_interactions.sort_values(by=['Id', 'Datetime'])

    # Calculate the duration between interactions in minutes
    user_interactions['Time_Diff'] = user_interactions['Datetime'].diff().dt.total_seconds().fillna(0) / 60

    # Identify blocked moments
    user_interactions['Block_Number'] = (user_interactions['Time_Diff'] > 60).cumsum()

    # Start the PUML content
    puml_content = "@startuml\n\n"

    # Define states by topic
    topics = user_interactions['Topic'].unique()
    for topic in topics:
        if pd.notna(topic):
            alias = topic.replace(" ", "_")
            puml_content += f'state "{topic}" as {alias}\n'

    # Add interactions within each state
    grouped = user_interactions.groupby('Topic')
    block_id = 1  # Sequential numbering for blocks
    transition_id = 1  # Sequential numbering for transitions
    for topic, group in grouped:
        if pd.isna(topic):
            continue

        alias = topic.replace(" ", "_")
        state_content = ""

        # Group interactions by block
        for block_num, block_group in group.groupby('Block_Number'):
            actions = ', '.join(block_group['Classification'].dropna())
            if len(block_group) > 1:
                block_time = (block_group['Datetime'].iloc[-1] - block_group['Datetime'].iloc[0]).total_seconds() / 60
            else:
                block_time = 0  # Only one interaction in the block
            time_string = f"{block_time / 60:.1f} h" if block_time > 60 else f"{block_time:.1f} min"
            state_content += f"{block_id}: {actions} - {time_string}\\n"
            block_id += 1

        puml_content += f'{alias} : {state_content.strip()}\n'

    # Create numbered transitions
    previous_topic = None
    previous_time = None
    for i, row in user_interactions.iterrows():
        current_topic = row['Topic']
        time_diff = row['Time_Diff']

        if pd.notna(current_topic):
            if previous_topic:
                previous_alias = previous_topic.replace(" ", "_")
                current_alias = current_topic.replace(" ", "_")

                if current_topic == previous_topic:
                    # Spacing and Retrieval
                    if time_diff > 60:
                        spacing_time = f"{time_diff / 60:.1f} h" if time_diff > 60 else f"{time_diff:.1f} min"
                        puml_content += f'{previous_alias} --> {current_alias} : {transition_id}: spacing and retrieval ({spacing_time})\n'
                        transition_id += 1
                else:
                    if time_diff > 60:
                        # Spacing and Interleaving
                        spacing_time = f"{time_diff / 60:.1f} h" if time_diff > 60 else f"{time_diff:.1f} min"
                        puml_content += f'{previous_alias} --> {current_alias} : {transition_id}: interleaving and spacing ({spacing_time})\n'
                    else:
                        # Interleaving
                        puml_content += f'{previous_alias} --> {current_alias} : {transition_id}: interleaving\n'
                    transition_id += 1

            previous_topic = current_topic
            previous_time = time_diff

    # Finalize the diagram
    puml_content += "\n@enduml"

    # Write to the output file
    with open(output_puml_path, 'w') as file:
        file.write(puml_content)

    print(f".puml file generated at: {output_puml_path}")


# Example usage
input_csv = "68result.csv"  # Replace with the path to your CSV file
output_puml = "detailed_corrected_diagram.puml"  # Replace with the path to the generated .puml file

generate_detailed_diagram_with_correct_numbering(input_csv, output_puml)
