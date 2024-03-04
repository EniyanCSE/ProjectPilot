import streamlit as st
import pandas as pd
import os
import time

# Function to check if the Excel file exists, and create it if not
def create_excel_file(file_path):
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=["Project Name", "Description", "Assigned Team Members", "Due Date", "Task Dependencies"])
        df.loc[1] = ["Test", "", "", None, ""]
        df.to_excel(file_path, index=False)
        return True
    return False

# Function to load data from Excel file into DataFrame
def load_data(file_path):
    df = pd.read_excel(file_path)
    return df

# Function to save DataFrame to Excel file
def save_data(df, file_path):
    df.to_excel(file_path, index=False)

# Function to add new project to Excel file
def add_new_project(project_name, file_path):
    print("Adding new project:", project_name)
    df = load_data(file_path)
    new_row_index = df.shape[0]
    df.loc[new_row_index, "Project Name"] = project_name
    print("DataFrame after adding new project:\n", df)  # Print DataFrame after adding new project
    save_data(df, file_path)
    print("Data saved successfully.")


# Main function
def main():
    st.title("Project Task List Manager")

    # Check if Excel file exists and create it if not
    file_path = "project_task_list.xlsx"
    excel_created = create_excel_file(file_path)

    # Load data from Excel file
    df = load_data(file_path)

    # Initialize selected_project_name
    selected_project_name = None

    # Sidebar
    st.sidebar.header("Options")
    if df.empty or excel_created:
        st.sidebar.write("No projects created.")
    else:
        selected_project_name = st.sidebar.selectbox("Select Project:", df["Project Name"].unique())

    # Display project details if selected_project_name is not None
    if selected_project_name is not None:
        st.subheader(f"Project Details: {selected_project_name}")
        selected_project_data = df[df["Project Name"] == selected_project_name].iloc[0]
        project_name = st.text_input("Project Name:", selected_project_name)
        description = st.text_area("Description:", selected_project_data["Description"])
        assigned_team_members = st.text_input("Assigned Team Members:", selected_project_data["Assigned Team Members"])

        # Handle Due Date
        due_date = selected_project_data["Due Date"]
        if pd.notnull(due_date):
            due_date = pd.to_datetime(due_date)
        else:
            due_date = None
        due_date = st.date_input("Due Date:", due_date)

        task_dependencies = st.text_area("Task Dependencies:", selected_project_data["Task Dependencies"])

        # Update DataFrame with user input
        df.loc[df["Project Name"] == selected_project_name, "Project Name"] = project_name
        df.loc[df["Project Name"] == project_name, "Description"] = description
        df.loc[df["Project Name"] == project_name, "Assigned Team Members"] = assigned_team_members
        df.loc[df["Project Name"] == project_name, "Due Date"] = due_date
        df.loc[df["Project Name"] == project_name, "Task Dependencies"] = task_dependencies

        # Save DataFrame to Excel file
        save_data(df, file_path)

    # Create new project button
    if st.sidebar.button("Create New Project"):
        new_project_name = st.sidebar.text_input("Enter Project Name:")
        if new_project_name.strip():
            add_new_project(new_project_name, file_path)
            st.sidebar.success("New project created successfully!")

            # Reload the app to reflect the changes
            st.rerun()

if __name__ == "__main__":
    main()
