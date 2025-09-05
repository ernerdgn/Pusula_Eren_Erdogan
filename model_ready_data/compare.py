import pandas as pd

def compare_excel_files(file1, file2):
    #file not found error handle
    try:
        xls1 = pd.ExcelFile(file1)
        xls2 = pd.ExcelFile(file2)
    except FileNotFoundError as e:
        print(f"Error: {e}. Please make sure both files are in the correct path.")
        return False

    sheets1 = xls1.sheet_names
    sheets2 = xls2.sheet_names

    if set(sheets1) != set(sheets2):
        print("different sheet names")
        print(f"'{file1}' sheets: {sorted(sheets1)}")
        print(f"'{file2}' sheets: {sorted(sheets2)}")
        return False

    identical = True
    for sheet_name in sheets1:
        print(f"=== comparing sheet: {sheet_name} ===")
        
        df1 = pd.read_excel(xls1, sheet_name=sheet_name)
        df2 = pd.read_excel(xls2, sheet_name=sheet_name)

        if set(df1.columns) != set(df2.columns):  # same columns?
            print(f"{sheet_name} columns' differ")
            print(f"columns in '{file1}': {sorted(list(df1.columns))}")
            print(f"columns in '{file2}': {sorted(list(df2.columns))}")
            identical = False
            continue

        print(f"sheets has matching columns")
        
        df2_reordered = df2[df1.columns]  # reorder columns to compare

        if df1.equals(df2_reordered):  # check rows if same
            print(f"sheet {sheet_name} is identical")
        else:
            print(f"sheet {sheet_name} has differences")
            identical = False

            try:  # find differences
                pd.testing.assert_frame_equal(df1, df2_reordered)
            except AssertionError as e:
                print("differences: ")
                print(e)
                print("\n")


    return identical

if __name__ == "__main__":
    # file_path1 = input(str("first file name: "))  #'model_ready_data1.xlsx'
    # file_path2 = input(str("second file name: "))
    file_path1 = 'model_ready_data.xlsx'
    file_path2 = 'model_ready_data_REFACTORED.xlsx'
    
    are_files_identical = compare_excel_files(file_path1, file_path2)

    print("\n=== RESULT ===")
    if are_files_identical:
        print("excel files are identical")
    else:
        print("excel files are NOT identical")