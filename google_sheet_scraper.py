import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Customizable_RT_Dashboard-36ebdf31ef48.json', scope) #Change to your downloaded JSON file name 
client = gspread.authorize(creds)

# List of our spreadsheet
spreadsheets = ['ITB 3.5 (Responses)']

# Scrapping the spreadsheet

def main(spreadsheets):

    df = pd.DataFrame()

    for spreadsheet in spreadsheets:
        #Open the Spreadsheet
        sh = client.open(spreadsheet)

		#Get all values in the first worksheet
        worksheet = sh.get_worksheet(0)
        data = worksheet.get_all_values()

		#Save the data inside the temporary pandas dataframe
        df_temp = pd.DataFrame(columns = [i for i in range(len(data[0]))])
        for i in range(1,len(data)):
            df_temp.loc[len(df_temp)] = data[i]
		
		#Convert column names
        column_names = data[0]
        df_temp.columns = [convert_column_names(x) for x in column_names]

		#Data Cleaning
        df_temp = df_temp.drop_duplicates().reset_index(drop=True) # Drop Duplicate
		
        #Data Preprocessing

        df_temp["Know Industry 4.0"] = df_temp["Know Industry 4.0"].replace({'Ya':'Yes','Tidak':'No'})
        

        # Encoding for "Why Ready of Not" and "ITB Should Teach"
        value_list_why_ready_or_not = ["Skill coding", "Kemampuan big data analytics", "Kemampuan machine learning", "Kreatifitas", "Manajemen manusia", "Berpikir kritis", "Saya tidak siap"]
        value_list_itb_should_teach = ["Skill coding", "Kemampuan big data analytics", "Kemampuan machine learning", "Kreatifitas", "Manajemen manusia", "Berpikir kritis", "ITB tidak mempersiapkan saya"]

        
        # For "Why Ready or Not"
        for value in value_list_why_ready_or_not :
            
            vec_temp = []

            for ans in df_temp["Why Ready or Not Ready"]:
                if value in ans:
                    vec_temp.append(1)
                else:
                    vec_temp.append(0)

            # Change value into english

            if value == "Kemampuan big data analytics" :
                value = "Big Data Skills"
            elif value == "Kemampuan machine learning" :
                value = "Machine Learning Skills"
            elif value == "Kreatifitas" :
                value = "Creativity"
            elif value == "Manajemen manusia" :
                value = "People Management"
            elif value == "Berpikir kritis" :
                value = "Critical Thinking"
            
            



            # Import as new columns
            if (value == "Saya tidak siap") :
                df_temp["Not Ready"] = vec_temp
            else :
                df_temp["Because "+str(value)] = vec_temp

            
        
        # For "ITB Should Teach"
        for value in value_list_itb_should_teach :
            
            vec_temp = []

            for ans in df_temp["Why Ready or Not Ready"]:
                if value in ans:
                    vec_temp.append(1)
                else:
                    vec_temp.append(0)

            # Change value into english

            if value == "Kemampuan big data analytics" :
                value = "Big Data Skills"
            elif value == "Kemampuan machine learning" :
                value = "Machine Learning Skills"
            elif value == "Kreatifitas" :
                value = "Creativity"
            elif value == "Manajemen manusia" :
                value = "People Management"
            elif value == "Berpikir kritis" :
                value = "Critical Thinking"
            elif value == "ITB tidak mempersiapkan saya" :
                value = "Doesn't Provide"
            
            



            # Import as new columns
            if (value == "Saya tidak siap") :
                df_temp["Not Ready"] = vec_temp
            else :
                df_temp["Should "+str(value)] = vec_temp
                

        # Delete "Why Ready of Not" and "ITB Should Teach" features

        df_temp = df_temp.drop(["Why Ready or Not Ready"] , axis= 1)
        df_temp = df_temp.drop(["ITB Should Teach"] , axis= 1)


        

		#Feature Engineering
       
		
		#Convert to timestamp
        df_temp['filling date'] = pd.to_datetime(df_temp['filling date'])

		#Concat Dataframe
        df = pd.concat([df,df_temp])	

		#API Limit Handling
        time.sleep(5)


    df = df.sort_values(by=['filling date']).reset_index(drop=True)

    df.to_csv('survey_data.csv',index=False)


def convert_column_names(x):
    if x == 'Apakah Anda mahasiswa/i ITB? (jika tidak, tolong jangan melanjutkan pengisian form ini)':
	    return 'university'
    elif x == 'Timestamp':
	    return 'filling date'
    elif x == 'Tahun berapa Anda masuk ke ITB?':
	    return 'Batch Year'
    elif x == 'Fakultas':
	    return 'Faculty'
    elif (x == 'Dari fakultas/prodi manakah Anda? (Jika TPB, tolong tuliskan fakultas. Jika bukan TPB, tolong tuliskan prodi)') :
	    return 'Subject'
    elif (x == 'Apakah Anda tahu apa itu industri 4.0?') :
	    return 'Know Industry 4.0'
    elif (x == 'Menurut Anda, seberapa siapkah Anda dalam menghadapi Industri 4.0?') :
	    return 'Readiness'
    elif (x == 'Mengapa Anda merasa siap/tidak siap? (pilihlah kemampuan berikut yang membuat Anda siap, boleh ditambah)') :
	    return 'Skill Needed'
    elif (x == 'Menurut Anda, seberapa besar kontribusi ITB dalam mempersiapkan Anda menuju Revolusi Industri 4.0?') :
	    return 'ITB Contribution'
    elif (x == 'Bagaimana ITB mempersiapkan Anda dalam menghadapi Revolusi Industri 4.0? (pilih kemampuan dibawah ini yang Anda dapatkan dari ITB, boleh menambah opsi)') :
	    return 'ITB Should Teach'
    elif (x == 'S') :
	    return 'Why Ready or Not Ready'
    else:
	    return x


if __name__ == '__main__':
	print('Scraping Data From Google Sheets.......')
	main(spreadsheets)	