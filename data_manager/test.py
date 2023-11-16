import re

string = \
"""
<<<MODULE>>><<<PATH>>>/EPB FIAT Ducato MY22 Tailor/02 System Specifications/02 System Design/SyDesign<<<BASELINE>>><<<VERSION>>>6.1-<<<USER>>>Z0000193<<<DATE>>>16 November 2021<<<ANNOTATION>>>16.11.2021 :
JKBaseline created for Fiat Ducato637 NAFTA DVR.<<<ATTRIBUTE>>>010_Object Type<<<ATTRIBUTE>>>011_DXL_Object State<<<ATTRIBUTE>>>011_Object State<<<ATTRIBUTE>>>012_Analysis Comment<<<ATTRIBUTE>>>013_DXL_Functional 
Safety Category<<<ATTRIBUTE>>>014_Requirement Source Comment<<<ATTRIBUTE>>>015_CM Reference<<<ATTRIBUTE>>>016_(Sub)System<<<ATTRIBUTE>>>017_Feature Increment<<<ATTRIBUTE>>>020_Review Assignment<<<ATTRIBUTE>>>
021_Review Agreed<<<ATTRIBUTE>>>022_Review Not Agreed<<<ATTRIBUTE>>>023_Review Comment<<<ATTRIBUTE>>>050_Test Department<<<ATTRIBUTE>>>051_VerificationMethod<<<ATTRIBUTE>>>053_TestResult<<<ATTRIBUTE>>>
057_TestComment<<<ATTRIBUTE>>>156_Test ID<<<ATTRIBUTE>>>802_Comment<<<ATTRIBUTE>>>820_EPBi Variant<<<ATTRIBUTE>>>821_Customer Visibility<<<ATTRIBUTE>>>822_Cross-Exchange Requirements<<<ATTRIBUTE>>>
824_Exclusive Platform<<<ATTRIBUTE>>>840_Responsible Stakeholder<<<ATTRIBUTE>>>841_Requirements State Subsystem<<<ATTRIBUTE>>>842_Subsystem Comment<<<ATTRIBUTE>>>843_Requirements State Customer
<<<ATTRIBUTE>>>844_Customer Comment<<<ATTRIBUTE>>>846_Project Adaption<<<ATTRIBUTE>>>848_Subsystem ID<<<ATTRIBUTE>>>881_DXL_Safety Goal<<<ATTRIBUTE>>>894_SuRE Review Check<<<ATTRIBUTE>>>Absolute Number
<<<ATTRIBUTE>>>Created By<<<ATTRIBUTE>>>Created On<<<ATTRIBUTE>>>Created Thru<<<ATTRIBUTE>>>deprecated - TRW Verification Method<<<ATTRIBUTE>>>DeXI_CoreObjectID_reqif<<<ATTRIBUTE>>>DeXI_Linkinfos
<<<ATTRIBUTE>>>DeXI_Modifications<<<ATTRIBUTE>>>DeXI_ModifiedAttribs<<<ATTRIBUTE>>>DeXI_ObjectType<<<ATTRIBUTE>>>DeXI_repl_ID<<<ATTRIBUTE>>>DeXI_SpecObjectID_reqif<<<ATTRIBUTE>>>DeXI_viewChapNum
<<<ATTRIBUTE>>>Last Modified By<<<ATTRIBUTE>>>Last Modified On<<<ATTRIBUTE>>>Object Heading<<<ATTRIBUTE>>>Object ID from Original<<<ATTRIBUTE>>>Object Short Text<<<ATTRIBUTE>>>Object Text<<<ATTRIBUTE>>>
Object Text_DXL<<<ATTRIBUTE>>>OLE<<<ATTRIBUTE>>>OLEIconic<<<ATTRIBUTE>>>Picture<<<ATTRIBUTE>>>PictureName<<<ATTRIBUTE>>>PictureNum<<<ATTRIBUTE>>>TableBottomBorder<<<ATTRIBUTE>>>TableCellAlign<<<ATTRIBUTE>>>
TableCellWidth<<<ATTRIBUTE>>>TableChangeBars<<<ATTRIBUTE>>>TableLeftBorder<<<ATTRIBUTE>>>TableLinkIndicators<<<ATTRIBUTE>>>TableRightBorder<<<ATTRIBUTE>>>TableShowAttrs<<<ATTRIBUTE>>>TableShowBookform<<<ATTRIBUTE>>>
TableShowWide<<<ATTRIBUTE>>>TableTopBorder<<<ATTRIBUTE>>>TableType<<<REQUIREMENT>>><<<ID>>>EPBi-Fiat_Ducato_MY22-SyDesign_1<<<LEVEL>>>1<<<HEADING>>>Introduction<<<COLUMN>>>Heading<<<COLUMN>>>n/a<<<COLUMN>>>
<<<COLUMN>>>EPBi FSS
Brake Assy
EPBi Host<<<COLUMN>>>n/a<<<COLUMN>>><<<COLUMN>>><<<REQUIREMENT>>><<<ID>>>EPBi-Fiat_Ducato_MY22-SyDesign_6753<<<LEVEL>>>2<<<HEADING>>>Purpose<<<COLUMN>>>Heading<<<COLUMN>>>n/a<<<COLUMN>>><<<COLUMN>>>EPBi FSS
Brake Assy

"""





baseline = {}

baseline_match = re.search(r"<<<BASELINE>>>(.+?)<<<ATTRIBUTE>>>", string, re.DOTALL)
baseline_string = baseline_match.group(1)

baseline_version = re.search(r"<<<VERSION>>>(.+?)<<<", baseline_string)

baseline_user = re.search(r"<<<USER>>>(.+?)<<<", baseline_string)
baseline_date = re.search(r"<<<DATE>>>(.+?)<<<", baseline_string)
baseline_annotation = re.search(r"<<<ANNOTATION>>>(.+)", baseline_string, re.DOTALL)

baseline["version"] = baseline_version.group(1)
baseline["user"] = baseline_user.group(1)
baseline["date"] = baseline_date.group(1)
baseline["annotation"] = baseline_annotation.group(1)

print(baseline)