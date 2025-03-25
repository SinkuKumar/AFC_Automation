from download_reports_sequential_class import ReportETL

reports = {
    "CNT_27": {
        "FROM_DATE": "01/01/2021",
        "TO_DATE": "02/02/2021"
    },
    
}

for report, dates in reports.items():
    print(f"{report}: {dates['FROM_DATE']} - {dates['TO_DATE']}")

client_id, client_name, username, password = [3698, 'AFC-Mandeep', 'sjalan@zca10', 'Graphx@222']
etl_reports = ReportETL('analytics_db', client_id)
etl_reports.experity_login(username, password)
etl_reports.etl_cnt_27('01/01/2024', '02/02/2024')
etl_reports.experity_logout()