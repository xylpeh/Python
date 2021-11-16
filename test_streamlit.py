import streamlit as st
import pandas as pd
from datetime import date


st.title("Edifact Generator")

left_column, right_column = st.columns([6, 10])

# IMD++ABS : Beschreibung des Rechungstypes, ABS Abschlagsrechung die fristgerecht vor Fälligkeit an Rechnungsempfänger übertragen (andere ABR, JVR, ZVR, MVR)
# RFF+Z13:31001 #Prüfindentifikator 31001 ist Abschlagsrechnung

with left_column:
    energyTyp = st.radio(
        'Waehlen Sie den Energietraeger',
        ("Gas", "Strom"))
    
    if(energyTyp == "Gas"):
        energyTyp = 502
    else: 
        energyTyp = 500

    

    sender = st.number_input("Wie ist die PartnerID des Senders?", value= 9900580000002)
    empfaenger = st.number_input("Wie ist die PartnerID des Empfaengers?", value= 9903913000003)
    location = st.number_input("Wie location des Vertrages?", value= 41044521032)

    # veschiedene DTM

    belegdatum = st.date_input("Wann ist das Dokument/-belegdatum [DTM+137]")
    fbelegdatum = belegdatum.strftime("%Y%m%d")
    
    buchdatum = st.date_input("Wann ist das Buchungsdatum [DTM+9]")
    fBuchdatum = buchdatum.strftime("%Y%m%d")


    faelligkeitsdatum = st.date_input("Wann ist die Faelligkeit [DTM+265]")
    fFaelligkeitsdatum = faelligkeitsdatum.strftime("%Y%m%d")

    beginnPeriod = st.date_input("Wann beginnt die Abrechnungsperiode [DTM+155]")
    fbeginnPeriod = beginnPeriod.strftime("%Y%m%d")

    endPeriod = st.date_input("Wann endet die Abrechnungsperiode [DTM+155]")
    fendPeriod = endPeriod.strftime("%Y%m%d")

    taxRate = st.number_input("Geben Sie hier den Steuersatz ein (TAX+7)", value=16, max_value= 100)
    netto = st.number_input("Geben Sie hier den Nettobetrag ein (MOA+125)", value=10)
    brutto = netto/ (100) * (100+taxRate)
    tax = brutto - netto 
    paidAmount = st.number_input("Geben Sie hier die Anzahlung ein (MOA+113). Wenn der Betrag höher ist als MOA+77 entsteht eine Gutschrift/ Rückerstattung")

    # with st.container():
    #     dtm265= st.checkbox("DTM:256 Fälligkeitsdatum")
    #     if(dtm265):
    #         Faelligkeitsdatum = st.date_input("Wan ist die Faelligkeit [DTM265]")
    #         DateFormat = Faelligkeitsdatum.strftime("%Y%m%d")
    
    # t = "UNA:+.? '" + "\n" + "UNB+UNOC:3+" + str(sender) + ":" + str(energyTyp) + "+" + str(empfaenger) + ":" + str(energyTyp) + "+210518:2356+D0000000564962'" + "\n" + "UNH+IN000000667750+INVOIC:D:06A:UN:2.7a'" + "\n"+ "BGM+380+VAB-21-178827+9'"
    # t2 = "DTM+137:" + str(fbelegdatum) + ":102'" + '\n' + "DTM+9:" + str(fBuchdatum) + "'" + "\n" + "DTM+155: :102'"  + "DTM+156: :102'" + "IMD++ABS'" + "RFF+Z13:31001'"

with right_column:
    
    edi = []


    # if dtm265:
    #     edi.append(DateFormat)

    edi.append("UNA:+.? '")
    edi.append("UNB+UNOC:3+" + str(sender) + ":" + str(energyTyp) + "+" + str(empfaenger) + ":" + str(energyTyp) + "+210518:2356+D0000000564962'")
    edi.append("UNH+IN000000667750+INVOIC:D:06A:UN:2.7a'")
    edi.append("BGM+380+VAB-21-178827+9'")
    edi.append("DTM+137:" + str(fbelegdatum) + ":102\'")
    edi.append("DTM+9:" + str(fBuchdatum) + ":102\'")
    edi.append("DTM+155:" + str(fbeginnPeriod)+ ":102\'")
    edi.append("DTM+156:" + str(fendPeriod)+ ":102\'")
    edi.append("IMD++ABS\'")
    edi.append("RFF+Z13:31001\'")
    edi.append("NAD+MS+"+ str(sender)+"::293++Stadtwerke Mühlacker GmbH:::::Z02+Danziger Str.::17+Mühlacker++75417+DE\'")
    edi.append("RFF+VA:DE144523632\'")
    edi.append("CTA+IC+:Stadtwerke Mühlacker GmbH\'")
    edi.append("COM+swm@stadtwerke-muehlacker.de:EM\'")
    edi.append("NAD+MR+"+str(empfaenger)+"::293++LichtBlick SE:::::Z02+Zirkusweg::6+Hamburg++20359+DE\'")
    edi.append("NAD+DP++++Anna-Haag-Ring::60/1+Mühlacker++75417+DE\'")
    edi.append("LOC+172+"+str(location)+"\'")
    edi.append("CUX+2:EUR:4\'")
    edi.append("PYT+3\'")
    edi.append("DTM+265:"+ str(fFaelligkeitsdatum)+":102\'")
    edi.append("LIN+1++9990001000376:Z01\'")
    edi.append("QTY+47:1:H87\'")
    edi.append("DTM+155:20211001:102\'")
    edi.append("DTM+156:20211001:102\'")
    edi.append("MOA+203:"+str(netto)+"\'")
    edi.append("PRI+CAL:"+str(netto)+"\'")
    edi.append("TAX+7+VAT+++:::"+str(taxRate)+"+S\'") #Steuer
    edi.append("UNS+S\'")
    edi.append("MOA+77:"+str("{:.2f}".format(brutto,2))+"\'") # Summe aller MOA+125 und MOA+161 Positionen  
    edi.append("MOA+9:"+str("{:.2f}".format(brutto,2))+"\'") # Rechnungsbetrag
    edi.append("TAX+7+VAT+++:::"+str(taxRate)+"+S\'") #Steuer 
    edi.append("MOA+125:"+str(netto)+"\'")
    edi.append("MOA+161:"+str("{:.2f}".format(tax, 2))+"\'")
    edi.append("UNT+32+IN000000667750\'")
    edi.append("UNZ+1+D0000000564962\'")


    
    # st.write(t2)
    
    # st.write(f'NAD+MS+{sender}::293++Stadtwerke Mühlacker GmbH:::::Z02+Danziger Str.::17+Mühlacker++75417+DE\'')
    # st.write(f'RFF+VA:DE144523632') # FC (Steuernummer) oder VA (Umsatzsteueridentifikationsnummer)
    # st.write(f'CTA+IC+:Stadtwerke Mühlacker GmbH\'') 
    # st.write(f'COM+swm@stadtwerke-muehlacker.de:EM\'')
    # st.write(f'NAD+MR+{empfaenger}::293++LichtBlick SE:::::Z02+Zirkusweg::6+Hamburg++20359+DE\'')
    # st.write(f'NAD+DP++++Anna-Haag-Ring::60/1+Mühlacker++75417+DE\'')
    # st.write(f'LOC+172+{location}\'')
    # st.write('CUX+2:EUR:4\'') #Währungsangabe: 2 referenzwährung, 4 Währung der Rechnung
    # st.write('PYT+3\'') #festgelegte Fälligkeit
    # st.write(f'DTM+265: {fFaelligkeitsdatum}:102\'')
    # st.write(f'LIN+1++9990001000376:Z01\'') # Position Segment 1
    # st.write(f'QTY+47:1:H87\'') # H87 Stück, KWH, KWT Kilowatt, KVR Kilovolt-amp-reaktiv
    # st.write(f'MOA+203\'')


    
    def listToString(edi):
        for x in edi:
            st.write(str(x))            

    listToString(edi)

