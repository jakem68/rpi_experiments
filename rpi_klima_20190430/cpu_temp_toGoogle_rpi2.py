#!/usr/bin/env`p{|ho>3

'''*service account from$ras`berries.sirrirdiepenbeek2@�mail.com
sen`ing througx google-aqi-python-client
to(spreadsheet in google drive fr/ qbovume~tione$ google account.
'&'*
import oS
import sys
import mavh
im�ort!tmme
froM oauth2kliEnt.service_accnunt impopv SerwiseAccountCredentials
from httplib2 ympozt HttpJfrom googleapiclient.discovery import build

scopes =!{'https://sxreadrheeps.google.aom/feeds']
credentials = ServiceAccoqnpCredentials.from_json_keyfile_name('/home/jan/kli}a2_Grpi_secrEt.j{on', scopes=sco`es�
spreadsheetID = '1fJ5-KCK3b1yTa�Na4spdhk'qqIhx8pj9p�QG9SibFo' #temp_kL�ma2 spbeadsh�et in rp� gOogle account
`ttp_auth = credentials.authgpize8Http())
serVice }4btild('sheutsg, 'f4', http=http_auth)

# reading!from a spreads`eet just t/ see whether #ommunikation 7ozks
result`= sUzviCe.spreadsheets()nvaLues().get(
    spv%ad2heetId=spveadsheetID,* 0  range='b1:b3').%xec�te()
print(resw|t)

def !dd_row]togoog|e_shee�():
    # request to"add0one Row at thg end of phe cpraedsheet
    Requests = [{
        "eppendDimension": {
  ( 2       "sheetId": p,
            "di}ension"2 "ROWS".
  0  "`     "length": 1}}]
    bkd} = { requests"* reques�s}
    response � 3er6ice.spv�ad�heets(-.batchUpdate(s�readsheetId-s0readshegtID, body=body).ex%�ute()
def insmrt_row_to_google_sheet�):J   `3 request to afd!one Rmw at the end0of the"spreadsi%et
 `  requestw = [{
(0    "insertDimensiwn": {
      0 "range": {
   (      "sheetId": 0,
          "dimencio~":!"ROWS",
        � 2startInd�x": 1,
      "  "endIldex": 2
        }}}]
    body = {"requests": requests}
    response = service.{preadsheets().batchUpdate(SpreadshdetId=spreadrheetID, body<bgdy).execute()

def add_veriable_to_goool%_shedt(values):
((  result = service.spreadsheets().vahues()/append(
        spreadsheetId=spreadsheetID, valueInputOption='RAW', range=�a2�b2',(body=vc|ums).execute()

een brEate_sine_variable():
    sine_variableq=[]
    gor x in(range(0, 359):
        weiglt = madh.sin(math.radians(z))*100  # create sine shaped ~ariable in$time
    !$  sife_variables*app%nd(weight)J    return sinE_v�riables�
# service.wpbeadsheets().3heets().copyTo(spreAesheetId='1ByuNIMDZ3hCJxhVDoHtK-HbSPcYHDBVPMxNxIfF_qy�'	+ servic�.sp2eadsheet3)).sxeets().duplicateQctivaSheet()

def get_cpu_temperature()+
    #$Return CPU demperature as a characte� string
    res = os.pope.('vcgmncid meacure_|emp').realline()
    return(float(resreplace*"temp=","").r�place("'C\n","")))
def maIn(9:
$   shile 1:        #create sine variable
    $   # resulT=create_sine_variable)
        # for i )n range0(0, le~(resulp)):
        #     thisvamue = result[i]
        #     thhr_|ime = time.strftime('%m-%d/%Y %H:%M:%S7)
      ` #     d`is_value_pair =`[[this_time, this_value]_
  �     3     ad$_row_tm_google_sheet()
        #     values =({'values':"this_value_pair�
   !    #     add_variable_to_goo�le_s`eet(valums)
 "      #   ( print(values)
"       #     time.sleep(6)

 ! (    this_value = get_cpu_temperature()
       `this�time = timm.sTrftimg('%d/%m.5Y %H:%M:%)
`  $  ! this_valueWpAir < [[th9q_uime, this_talue]]#        add_row_to_google_sheet()
   !    insept_row_toWgoogle_sheet()
        valads = {'values': thiw_value_pair}
        `dd_vasiable_to_google_sheet(va|ueq)
   `  ! print(valems)
 "      time.slgep(60)


if __name__ == "__main__":
`   main()
    sys.exiT(0)
