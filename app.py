from sklearn.preprocessing import OrdinalEncoder

from flask import Flask, render_template,url_for, request
import os,joblib #to load the ML model


#Vectorizers
House_Summ_Cons_vectorizer = open(os.path.join("static/Models/Household_Summer_model_.pkl"),"rb") #read the pickle file
House_Summ_Cons_model = joblib.load(House_Summ_Cons_vectorizer)

House_Win_Cons_vectorizer = open(os.path.join("static/Models/Household_Winter_model_.pkl"),"rb") #read the pickle file
House_Win_Cons_model = joblib.load(House_Win_Cons_vectorizer)

Community_Summ_Cons_vectorizer = open(os.path.join("static/Models/Community_Summer_model_.pkl"),"rb") #read the pickle file
Community_Summ_Cons_model = joblib.load(Community_Summ_Cons_vectorizer)

Community_Win_Cons_vectorizer = open(os.path.join("static/Models/Community_Winter_model_.pkl"),"rb") #read the pickle file
Community_Win_Cons_model = joblib.load(Community_Win_Cons_vectorizer)

app = Flask(__name__)

prediction_labels ={1:{"value":"First segment", "range": "from 0 to 50 Kw"},
		                   2 : {"value":'Second segment', "range": "from 51 to 100 kw"},
		                   3 : {"value":'Third segment', "range": "from 101 to 200 kw"}, 
		                   4 : {"value":'Fourth segment', "range": "from 201 to 350 kw"},
		                   5 : {"value":'Fifth segment', "range":"from 351 to 650 kw"}, 
		                   6 : {"value":'Sixth segment', "range":"from 651 to 1000 kw"},
		                   7 : {"value":'Seventh segment', "range": "more than 1000 kw"}}

arab_prediction_labels ={1:{"value":"الشريحة الأولى", "range": "من 0 إلى 50 ك.و"},
		                   2 : {"value":'الشريحة الثانية', "range": "من 51 إلى 100 ك.و"},
		                   3 : {"value":'الشريحة الثالثة', "range": "من 101 إلى 200 ك.و"}, 
		                   4 : {"value":'الشريحة الرابعة', "range": "من 201 إلى 350 ك.و"},
		                   5 : {"value":'الشريحة الخامسة', "range":"من 251 إلى 650 ك.و"}, 
		                   6 : {"value":'الشريحة السادسة', "range":"من 651 إلى 1000 ك.و"},
		                   7 : {"value":'الشريحة السابعة', "range": "أكثر من 1000 ك.و"}}

# prediction_labels ={'First segment': 1,'Second segment': 2,
# 		                    'Third segment': 3, 'Fourth segment': 4,
# 		                    'Fifth segment': 5, 'Sixth segment': 6,
# 		                    'Seventh segment': 7}

arab_Lang_Flag = False;

print("Helloooo")
def get_keys(val,my_dict):
	for key, values in my_dict.items():
		if val == key:
			# print("fff",values)
			return values["value"], values["range"]

# result=get_keys (2,prediction_labels)
# print("result ya rub", result[0])	
# print("result ya rub.....", result[1])
def light_whrs_guide(Art_Light_Whrs,flag):

	if Art_Light_Whrs >2:
		if flag == False:
			return "High Artificial lighting working hours"
		else:
			return "ارتفاع عدد ساعات تشغيل الإضاءة الصناعية"

def fan_whrs_guide(Fan_Whrs,flag):
	if Fan_Whrs == 3:
		if flag == False:
			return "high fan working hours"
		else:
			return "ارتفاع عدد ساعات تشغيل المروحة"

def Ac_whrs_guide(AC_Whrs,flag):
	if AC_Whrs == 5 or AC_Whrs == 6 or AC_Whrs == 7:
		if flag == False:
			return "High AC working hours"
		else:
			return "ارتفاع عدد ساعات التكييف"

def heater_whrs_guide(Heater_Whrs,flag):
	if Heater_Whrs == 5 or Heater_Whrs == 6 or Heater_Whrs == 7:
		if flag == False:
			return "High heater working hours"
		else:
			return "ارتفاع عدد ساعات تشغيل السخان"

def motor_whrs_guide(motor_Whrs,flag):
	if motor_Whrs == 2 or motor_Whrs == 3:
		if flag == False:
			return "High motor working hours"
		else:
			return "ارتفاع عدد ساعات تشغيل الموتور"

def kettle_whrs_guide(Kettle_Whrs,flag):
	if Kettle_Whrs == 2 or Kettle_Whrs == 3:
		if flag == False:
			return "High kettle working hours"
		else:
			return "ارتفاع عدد ساعات تشغيل الغلاية"

def append_guide_results(arr):
	for value in arr:
		if arr:
			notes = notes.append(value)
	return value

@app.route('/about')
def about():
	return render_template('about.html')



@app.route('/')
def index():
	return render_template('index.html')


@app.route('/household_predict',methods=['GET','POST'])
def household_predict():
	if request.method == 'POST':
		Storey_No = float(request.form.get('Storey_No'))
		Rooms_No = float(request.form.get('Rooms_No'))
		Openings_No = float(request.form.get('Openings_No'))
		Floor_area = float(request.form.get('Floor_area'))
		Art_Light_Whrs = float(request.form.get('Art_Light_Whrs'))
		Householder_Educational_level = float(request.form.get('Householder_Educational_level'))
		No_of_appliances = float(request.form.get('No_of_appliances'))
		Fan_Whrs = float(request.form.get('Fan_Whrs'))
		AC_Whrs = float(request.form.get('AC_Whrs'))
		Family_members = float(request.form.get('Family_members'))
		Heater_Whrs = float(request.form.get('Heater_Whrs'))
		Washing_Mach_Whrs = float(request.form.get('washing_Mach_Whrs'))
		Motor_Whrs = float(request.form.get('Motor_Whrs'))
		Kettle_Whrs = float(request.form.get('Kettle_Whrs'))
		#Prediction
		
		House_Summ_prediction = House_Summ_Cons_model.predict([[Storey_No,Rooms_No,Openings_No,Floor_area,Art_Light_Whrs,
			Family_members,Householder_Educational_level,No_of_appliances,Fan_Whrs,AC_Whrs,Washing_Mach_Whrs]])
		House_Win_prediction = House_Win_Cons_model.predict([[Storey_No,Rooms_No,Openings_No,Floor_area,Art_Light_Whrs,Family_members,Householder_Educational_level
			,No_of_appliances,Motor_Whrs,Kettle_Whrs,Heater_Whrs,Washing_Mach_Whrs]])
		House_Summ_final_result = get_keys(House_Summ_prediction,prediction_labels)
		House_Win_final_result =  get_keys(House_Win_prediction,prediction_labels)
		note_results = [] 
		Art_light_note = light_whrs_guide(Art_Light_Whrs,arab_Lang_Flag)
		if Art_light_note:
			note_results.append(Art_light_note)
		fan_note = fan_whrs_guide(Fan_Whrs,arab_Lang_Flag)
		if fan_note:
			note_results.append(fan_note)

		Ac_note = Ac_whrs_guide(AC_Whrs,arab_Lang_Flag)
		if Ac_note:
			note_results.append(Ac_note)

		heater_note = heater_whrs_guide(Heater_Whrs,arab_Lang_Flag)
		if heater_note:
			note_results.append(heater_note)

		motor_note = motor_whrs_guide(Motor_Whrs,arab_Lang_Flag)
		if motor_note:
			note_results.append(motor_note)

		kettle_note = kettle_whrs_guide(Kettle_Whrs,arab_Lang_Flag)
		if kettle_note:
			note_results.append(kettle_note)

        

		# return render_template('household.html',House_Summ_final_result=House_Summ_final_result[0],
		# 	summ_range=House_Summ_final_result[1],House_Win_final_result=House_Win_final_result[0],
		# 	win_range=House_Win_final_result[1],note_results=note_results)
		return render_template('household.html',House_Summ_final_result=House_Summ_final_result[0]+" "+"  in range:"+" "+
			House_Summ_final_result[1],House_Win_final_result=House_Win_final_result[0]+" "+"  in range:"+" "+
			House_Win_final_result[1],note_results=note_results)

		####################################################################################################################################
@app.route('/arab_household_predict',methods=['GET','POST'])
def arab_household_predict():
	if request.method == 'POST':
		arab_Lang_Flag = True;
		print("Flag value is:",arab_Lang_Flag)
		Storey_No = float(request.form.get('Storey_No'))
		Rooms_No = float(request.form.get('Rooms_No'))
		Openings_No = float(request.form.get('Openings_No'))
		Floor_area = float(request.form.get('Floor_area'))
		Art_Light_Whrs = float(request.form.get('Art_Light_Whrs'))
		Householder_Educational_level = float(request.form.get('Householder_Educational_level'))
		No_of_appliances = float(request.form.get('No_of_appliances'))
		Fan_Whrs = float(request.form.get('Fan_Whrs'))
		AC_Whrs = float(request.form.get('AC_Whrs'))
		Family_members = float(request.form.get('Family_members'))
		Heater_Whrs = float(request.form.get('Heater_Whrs'))
		Washing_Mach_Whrs = float(request.form.get('washing_Mach_Whrs'))
		Motor_Whrs = float(request.form.get('Motor_Whrs'))
		Kettle_Whrs = float(request.form.get('Kettle_Whrs'))
		#Prediction
		
		House_Summ_prediction = House_Summ_Cons_model.predict([[Storey_No,Rooms_No,Openings_No,Floor_area,Art_Light_Whrs,
			Family_members,Householder_Educational_level,No_of_appliances,Fan_Whrs,AC_Whrs,Washing_Mach_Whrs]])
		House_Win_prediction = House_Win_Cons_model.predict([[Storey_No,Rooms_No,Openings_No,Floor_area,Art_Light_Whrs,Family_members,Householder_Educational_level
			,No_of_appliances,Motor_Whrs,Kettle_Whrs,Heater_Whrs,Washing_Mach_Whrs]])
		House_Summ_final_result = get_keys(House_Summ_prediction,arab_prediction_labels)
		House_Win_final_result =  get_keys(House_Win_prediction,arab_prediction_labels)
		note_results = [] 
		Art_light_note = light_whrs_guide(Art_Light_Whrs,arab_Lang_Flag)
		if Art_light_note:
			note_results.append(Art_light_note)
		fan_note = fan_whrs_guide(Fan_Whrs,arab_Lang_Flag)
		if fan_note:
			note_results.append(fan_note)

		Ac_note = Ac_whrs_guide(AC_Whrs,arab_Lang_Flag)
		if Ac_note:
			note_results.append(Ac_note)

		heater_note = heater_whrs_guide(Heater_Whrs,arab_Lang_Flag)
		if heater_note:
			note_results.append(heater_note)

		motor_note = motor_whrs_guide(Motor_Whrs,arab_Lang_Flag)
		if motor_note:
			note_results.append(motor_note)

		kettle_note = kettle_whrs_guide(Kettle_Whrs,arab_Lang_Flag)
		if kettle_note:
			note_results.append(kettle_note)

        

		# return render_template('household.html',House_Summ_final_result=House_Summ_final_result[0],
		# 	summ_range=House_Summ_final_result[1],House_Win_final_result=House_Win_final_result[0],
		# 	win_range=House_Win_final_result[1],note_results=note_results)
		return render_template('household-rtl.html',House_Summ_final_result=House_Summ_final_result[0]+" "+"  "+"وهي"+" "+
			House_Summ_final_result[1],House_Win_final_result=House_Win_final_result[0]+" "+" "+"وهي"+" "+
			House_Win_final_result[1],note_results=note_results)



		####################################################################################################################################

@app.route('/community_predict',methods=['GET','POST'])
def community_predict():
	if request.method == 'POST':
		land_type = float(request.form.get('land_type'))
		overcrowding = float(request.form.get('overcrowding'))
		household_size = float(request.form.get('household_size'))
		Summer_humidity = float(request.form.get('Summer_humidity'))
		Summer_Max_temp = float(request.form.get('Summer_Max_temp'))
		Summer_Min_temp = float(request.form.get('Summer_Min_temp'))
		Percent_of_pop_less_15 = float(request.form.get('Percent_of_pop_less_15'))
		Percent_of_pop_bet_15_to_less_60 = float(request.form.get('Percent_of_pop_bet_15_to_less_60'))
		Percent_of_pop_more_60 = float(request.form.get('Percent_of_pop_more_60'))
		Percent_of_higher_education = float(request.form.get('Percent_of_higher_education'))
		Percent_of_illiterate = float(request.form.get('Percent_of_illiterate'))
		Winter_humidity = float(request.form.get('Winter_humidity'))
		Winter_Avg_temp = float(request.form.get('Winter_Avg_temp'))
		Winter_Min_temp = float(request.form.get('Winter_Min_temp'))
		Percent_no_build_conn_elect = float(request.form.get('Percent_no_build_conn_elect'))
		Percent_depend_Elec_cooking = float(request.form.get('Percent_depend_Elec_cooking'))



		#Prediction
		
		Comm_Summ_prediction = Community_Summ_Cons_model.predict([[land_type,overcrowding,household_size,Summer_humidity,
			Summer_Max_temp,Summer_Min_temp,Percent_of_pop_less_15,Percent_of_pop_bet_15_to_less_60,Percent_of_pop_more_60,
			Percent_of_higher_education,Percent_of_illiterate]])
		Comm_Win_prediction = Community_Win_Cons_model.predict([[land_type,Percent_of_pop_less_15,Percent_of_pop_bet_15_to_less_60,
			Percent_of_pop_more_60,Percent_of_higher_education,Percent_of_illiterate,Winter_humidity,Winter_Avg_temp,Winter_Min_temp,
			Percent_no_build_conn_elect,overcrowding,household_size,Percent_depend_Elec_cooking]])
		Comm_Summ_final_result = get_keys(Comm_Summ_prediction,prediction_labels)
		Comm_Win_final_result =  get_keys(Comm_Win_prediction,prediction_labels)
		return render_template('community.html',Comm_Summ_final_result=Comm_Summ_final_result[0]+" "+"  in range:"+" "+
			Comm_Summ_final_result[1],Comm_Win_final_result=Comm_Win_final_result[0]+" "+"  in range:"+" "+Comm_Win_final_result[1])


###########################################################################################################################################

@app.route('/arab_community_predict',methods=['GET','POST'])
def arab_community_predict():
	if request.method == 'POST':
		land_type = float(request.form.get('land_type'))
		overcrowding = float(request.form.get('overcrowding'))
		household_size = float(request.form.get('household_size'))
		Summer_humidity = float(request.form.get('Summer_humidity'))
		Summer_Max_temp = float(request.form.get('Summer_Max_temp'))
		Summer_Min_temp = float(request.form.get('Summer_Min_temp'))
		Percent_of_pop_less_15 = float(request.form.get('Percent_of_pop_less_15'))
		Percent_of_pop_bet_15_to_less_60 = float(request.form.get('Percent_of_pop_bet_15_to_less_60'))
		Percent_of_pop_more_60 = float(request.form.get('Percent_of_pop_more_60'))
		Percent_of_higher_education = float(request.form.get('Percent_of_higher_education'))
		Percent_of_illiterate = float(request.form.get('Percent_of_illiterate'))
		Winter_humidity = float(request.form.get('Winter_humidity'))
		Winter_Avg_temp = float(request.form.get('Winter_Avg_temp'))
		Winter_Min_temp = float(request.form.get('Winter_Min_temp'))
		Percent_no_build_conn_elect = float(request.form.get('Percent_no_build_conn_elect'))
		Percent_depend_Elec_cooking = float(request.form.get('Percent_depend_Elec_cooking'))



		#Prediction
		
		Comm_Summ_prediction = Community_Summ_Cons_model.predict([[land_type,overcrowding,household_size,Summer_humidity,
			Summer_Max_temp,Summer_Min_temp,Percent_of_pop_less_15,Percent_of_pop_bet_15_to_less_60,Percent_of_pop_more_60,
			Percent_of_higher_education,Percent_of_illiterate]])
		Comm_Win_prediction = Community_Win_Cons_model.predict([[land_type,Percent_of_pop_less_15,Percent_of_pop_bet_15_to_less_60,
			Percent_of_pop_more_60,Percent_of_higher_education,Percent_of_illiterate,Winter_humidity,Winter_Avg_temp,Winter_Min_temp,
			Percent_no_build_conn_elect,overcrowding,household_size,Percent_depend_Elec_cooking]])
		Comm_Summ_final_result = get_keys(Comm_Summ_prediction,arab_prediction_labels)
		Comm_Win_final_result =  get_keys(Comm_Win_prediction,arab_prediction_labels)
		return render_template('community-rtl.html',Comm_Summ_final_result=Comm_Summ_final_result[0]+" "+": وهي"+" "+
			Comm_Summ_final_result[1],Comm_Win_final_result=Comm_Win_final_result[0]+" "+": وهي"+" "+Comm_Win_final_result[1])


############################################################################################################################################		

@app.route('/translate_arab',methods=['GET','POST'])
def translate_arab():
	
    return render_template('index_rtl.html')
@app.route('/translate_eng', methods=['GET','POSt'])
def translate_eng():
	return render_template('index.html')


@app.route('/redirect',methods=['GET','POST'])
def redirect():
	if request.method == 'POST':
		if request.form['submit'] == "Household":
			return render_template('household.html')
		elif request.form['submit'] == "Community":
			return render_template('community.html')

@app.route('/redirect_arab',methods=['GET','POST'])
def redirect_arab():
	if request.method == 'POST':
		if request.form['submit'] == "Household":
			return render_template('household-rtl.html')
		elif request.form['submit'] == "Community":
			return render_template('community-rtl.html')

        
if __name__ == '__main__':
	app.run(debug=True)
