import pandas as pd
import streamlit as st
import altair as alt
import numpy as np


def main():

    df = load_data()

    

    st.title("Is ITB Students Ready for Industry Revolution 4.0?")
    st.markdown("---")
    st.markdown("### Respondent Monitoring  Dashboard")
    st.markdown("#### By: Christofel Rio Goenawan")
	
    st.markdown("---")
    viz_type_filter = st.selectbox("How do you want to see?", ['Overview','Detailed Information'],0)

    if viz_type_filter == 'Overview':

        # Create overview statistics
        average_readiness = str(np.mean(df["Readiness"]))+(" / 5.0")
        many_not_ready = np.sum(df["Not Ready"])
        many_ready = len(df) - many_not_ready

        data = {'Average Readiness':[average_readiness], 'Number of Ready Students':[many_ready], 'Number of Not Ready':[many_not_ready]} 
        
        # Create DataFrame 
        df_stat = pd.DataFrame(data) 

        

        st.table(df_stat.assign(hack='').set_index('hack'))
  

        st.markdown("> Chart in this page shows the comparison of number of respondents who is feel ready or not")
        st.markdown("**Respondents: {}**".format(len(df)))
        

        variable_filter = st.selectbox("Variable Filter", ['No Filter','University',"Faculty", "Batch Year", "Know Revolution 4.0 or Not"],0)

        if variable_filter == 'No Filter':
            visualize_is_tested_comparison(df,None)
        elif variable_filter == 'University':
            visualize_is_tested_comparison(df,"university")
        elif variable_filter == "Faculty":
            visualize_is_tested_comparison(df,"Faculty")
        elif variable_filter == "Batch Year":
            visualize_is_tested_comparison(df,'Batch Year')
        elif variable_filter == "Know Revolution 4.0 or Not":
            visualize_is_tested_comparison(df,'Know Industry 4.0')
        else:
            st.write("Work in Progress..")


    elif viz_type_filter == 'Detailed Information':
        st.markdown("> Charts in this page are detailed information of Data")
        st.markdown("### Skills provided by ITB")

        skill_list = ["Skill coding", "Big Data Skills", "Machine Learning Skills", "Creativity", "People Management", "Critical Thinking"]

        data = {'Count':[]}
        # Create DataFrame 
        df_skill_provided = pd.DataFrame(data) 

        for skill in skill_list:
            df_skill_provided.loc[skill] = np.sum(df["Because "+str(skill)])

        df_skill_provided = df_skill_provided.sort_values(by=["Count"] , ascending = False)

        st.bar_chart(df_skill_provided, height=800,width=800)

        st.markdown("### Skills should be provided by ITB")

        df_skill_should_provided = pd.DataFrame(data) 

        for skill in skill_list:
            df_skill_should_provided.loc[skill] = np.sum(df["Should "+str(skill)])

        df_skill_should_provided = df_skill_should_provided.sort_values(by=["Count"] , ascending = False)

        st.bar_chart(df_skill_should_provided, height=800,width=800)


def load_data():
	df = pd.read_csv('survey_data.csv')

	df['filling date'] = pd.to_datetime(df['filling date']).dt.date

	return df


def visualize_is_tested_comparison(df,variable):
	
	if variable==None:
		df_grouped = df.groupby(['Readiness']).size().reset_index(name='count')

		bars = alt.Chart(df_grouped).mark_bar().encode(
			x = alt.X('Readiness:N'),
			y = alt.Y('sum(count):Q', stack='zero',title='count')
			)

		group_bars = alt.Chart(df_grouped).mark_bar().encode(
			x = alt.X('Readiness:N'),
			y = alt.Y('sum(count):Q', stack='zero',title='count'),
			tooltip = [alt.Tooltip('sum(count):Q',title='count')],
			color = alt.Color('Readiness')
			)

		text = bars.mark_text(dy=-10).encode(
			text = 'sum(count):Q'
			)

		group_text = alt.Chart(df_grouped).mark_text(dy=12,color='white').encode(
			x = alt.X('Readiness:N'),
			y = alt.Y('sum(count):Q', stack='zero'),
			detail = 'Readiness:N',
			text = alt.Text('sum(count):Q')
			)

		st.altair_chart((group_bars + text + group_text).properties(height=800,width=800,title='Comparison Between Readiness'))

	else:

		for _type in df[variable].unique():
			df_temp = df[df[variable]==_type]
			df_grouped = df_temp.groupby(['Readiness']).size().reset_index(name='count')

			bars = alt.Chart(df_grouped).mark_bar().encode(
				x = alt.X('Readiness:N'),
				y = alt.Y('sum(count):Q', stack='zero',title='count')
				)

			group_bars = alt.Chart(df_grouped).mark_bar().encode(
				x = alt.X('Readiness:N'),
				y = alt.Y('sum(count):Q', stack='zero',title='count'),
				tooltip = [alt.Tooltip('sum(count):Q',title='count')],
				color = alt.Color('Readiness')
				)

			text = bars.mark_text(dy=-10).encode(
				text = 'sum(count):Q'
				)

			group_text = alt.Chart(df_grouped).mark_text(dy=12,color='white').encode(
				x = alt.X('Readiness:N'),
				y = alt.Y('sum(count):Q', stack='zero'),
				detail = 'Readiness:N',
				text = alt.Text('sum(count):Q')
				)

			st.altair_chart((group_bars + text + group_text).properties(height=800,width=800,title='Comparison Between Readiness on ' + str(variable)+ " :" + str(_type)))





if __name__ == '__main__':
	main()