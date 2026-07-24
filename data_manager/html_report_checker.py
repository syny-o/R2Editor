def classify_references(html_report, references):
    report_lower = html_report.lower()
    covered = []
    missing = []
    for reference in references:
        target = covered if reference.lower() in report_lower else missing
        target.append(reference)
    return missing, covered
