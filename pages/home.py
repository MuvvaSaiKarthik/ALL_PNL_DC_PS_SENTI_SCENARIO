import streamlit as st
import datetime
import pandas as pd
import time
from streamlit_option_menu import option_menu

st.set_page_config(layout='wide')

def fetch_data_PNL():
    try:
        df = pd.read_csv('dropcopy_Dealer_PNL_mar_pinpout_scenario_sqlview.csv')
        df[['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL']] = df[
            ['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL']].round(2)
        return df
    except Exception as e:
        print(f'Error fetching the data: {str(e)}')
        return None


def style_dataframe_PNL(df):
    return df.style.applymap(
        lambda x: 'color: green' if x > 0 else ('color: red' if x < 0 else 'color: black'),
        subset=['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL', 'PL_D0.5U0.5',
                'PL_U0.5D0.5', 'PinPout', 'Actual', 'ExpOptVal', 'With_Exch']
    ).format(precision=2)


def style_dataframe_SENTI(df):
    return df.style.applymap(
        lambda x: 'background-color: yellow' if ((x < -350) & (x > -450)) else (
            'background-color: red; color: white' if x < -450 else 'background-color: white'),
        subset=['Senti_2003', 'Senti_2051', 'Senti_6760', 'Senti_9771']
    ).format(precision=0)


def style_dataframe_SCENARIO(df):
    return df.style.applymap(
        lambda x: 'color: green' if x > 0 else ('color: red' if x < 0 else 'color: black'),
        subset=['PL_D10U5', 'PL_D5U2', 'PL_D2U1.5', 'PL_D1U1',
                'PL_D0.5U0.5', 'PL_U0.5D0.5', 'PL_U1U0', 'PL_U2U1', 'PL_U5U2', 'PL_U10U5']
    )


def time_difference_in_minutes(dt1, dt2):
    timedelta = dt2 - dt1
    return (timedelta.total_seconds() // 60)


try:
    if st.session_state["my_input"] == 'VIKABH':

        logout = st.button('Logout')

        if logout:
            st.markdown('<span style="color: blue;">Please go to login in the side menu</span>', unsafe_allow_html=True)
            st.session_state["my_input"] = None

            exit(0)

        selected = option_menu(
            menu_title=None,
            options=['PNL', 'SENTI', 'Scenario'],
            default_index=0,  # default selected navigation
            orientation='horizontal'
        )

        if selected == 'PNL':
            st.title("PNL DASHBOARD")

            # create placeholders
            time_display_pnl = st.empty()
            time_delay_alert = st.empty()
            # total_dataframe_placeholder_pnl = st.empty()
            pnl_team_placeholder_pnl = st.empty()
            # pnl_dataframe_placeholder_pnl = st.empty()

            while True:
                try:
                    pnl = fetch_data_PNL()

                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    data_fetch_time = pnl['DT'].iloc[0]
                    del pnl['DT']

                    data_fetch_time = pd.to_datetime(data_fetch_time)
                    current_time_dt = pd.to_datetime(current_time)
                    time_diff_min = time_difference_in_minutes(current_time_dt, data_fetch_time)
                    time_diff_min = abs(time_diff_min)

                    page_updates = datetime.datetime.now().strftime('%S')

                    # Update time_display placeholder
                    time_display_pnl.write(f'Latest {page_updates}   |   PNL Time {data_fetch_time}', format='md')

                    # if time_diff_min > 3:
                    #     time_delay_alert.markdown('<span style="color: red">Data delay greater than 2 minutes!</span>',
                    #                               unsafe_allow_html=True)
                    # else:
                    #     time_delay_alert.write("")

                    if pnl is not None:
                        # Calculate and append totals row
                        pnl_team = pnl[['Team', 'Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL', 'PL_D0.5U0.5',
                                        'PL_U0.5D0.5', 'PinPout', 'Actual', 'ExpOptVal', 'With_Exch']].groupby(
                            by=['Team']).sum().reset_index()

                        # pnl_team[['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL', 'PL_D0.5U0.5',
                        #           'PL_U0.5D0.5', 'PinPout', 'Actual', 'ExpOptVal', 'With_Exch']] = pnl_team[
                        #     ['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL', 'PL_D0.5U0.5',
                        #      'PL_U0.5D0.5', 'PinPout', 'Actual', 'ExpOptVal', 'With_Exch']].astype(int)

                        total_pnl = pnl_team.select_dtypes(include=['number']).sum().reset_index()

                        total_pnl = pd.pivot_table(total_pnl, columns='index', values=0)

                        total_pnl['Team'] = 'Total'

                        total_pnl = total_pnl[['Team', 'Mrg', 'Y_PNL', 'E_PNL', 'O_PNL',
                                               'I_PNL', 'T_PNL', 'PL_D0.5U0.5', 'PL_U0.5D0.5', 'PinPout', 'Actual',
                                               'ExpOptVal', 'With_Exch']]

                        pnl = pnl[['Team', 'Name', 'Mrg', 'Y_PNL', 'E_PNL', 'O_PNL',
                                   'I_PNL', 'T_PNL', 'PL_D0.5U0.5', 'PL_U0.5D0.5', 'PinPout', 'Actual',
                                   'ExpOptVal', 'With_Exch']]

                        pnl_team = pnl_team[['Team', 'Mrg', 'Y_PNL', 'E_PNL', 'O_PNL',
                                             'I_PNL', 'T_PNL', 'PL_D0.5U0.5', 'PL_U0.5D0.5', 'PinPout', 'Actual',
                                             'ExpOptVal', 'With_Exch']]

                        # total_pnl[
                        #     ['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL', 'PL_D0.5U0.5', 'PL_U0.5D0.5', 'PinPout',
                        #      'Actual',
                        #      'ExpOptVal', 'With_Exch']] = total_pnl[
                        #     ['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL', 'PL_D0.5U0.5', 'PL_U0.5D0.5', 'PinPout',
                        #      'Actual',
                        #      'ExpOptVal', 'With_Exch']].astype(int)
                        #
                        #
                        # pnl_team[
                        #     ['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL', 'PL_D0.5U0.5', 'PL_U0.5D0.5', 'PinPout',
                        #      'Actual',
                        #      'ExpOptVal', 'With_Exch']] = pnl_team[
                        #     ['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL', 'PL_D0.5U0.5', 'PL_U0.5D0.5', 'PinPout',
                        #      'Actual',
                        #      'ExpOptVal', 'With_Exch']].astype(int)

                        pnl_team = pnl_team.sort_values(by='Mrg', ascending=False)

                        # remove wrong index
                        pnl_team.reset_index(inplace=True)
                        del pnl_team['index']
                        pnl_team.index = pnl_team['Team']
                        del pnl_team['Team']

                        # Create styled Data Frames
                        # total_styled_df = style_dataframe_PNL(total_pnl)
                        pnl_team_styled_df = style_dataframe_PNL(pnl_team)
                        # pnl_styled_df = style_dataframe_PNL(pnl)

                        # Update dataframe placeholder
                        # total_dataframe_placeholder_pnl.dataframe(total_styled_df, width=5000)
                        pnl_team_placeholder_pnl.dataframe(pnl_team_styled_df, height=500, width=5000)
                        # pnl_dataframe_placeholder_pnl.dataframe(pnl_styled_df, width=5000)

                    # Sleep for 3 seconds before the next update
                    time.sleep(3)

                except Exception as e:
                    print('Issue:', e)
                    time.sleep(1)
                    pass

        if selected == 'SENTI':
            st.title('DC PS SENTI')

            # Create placeholders for dynamic content
            time_display_senti = st.empty()
            time_delay_alert = st.empty()
            complete_placeholder_senti = st.empty()

            while True:
                try:
                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # Fetch data
                    complete_df = pd.read_csv('senti_ps.csv')
                    time_frame = complete_df['DT'].iloc[0]
                    del complete_df['DT']

                    time_frame = pd.to_datetime(time_frame)
                    current_time_dt = pd.to_datetime(current_time)
                    time_diff_min = time_difference_in_minutes(current_time_dt, time_frame)
                    time_diff_min = abs(time_diff_min)

                    page_updates = datetime.datetime.now().strftime('%S')

                    # Update time_display placeholder
                    time_display_senti.write(f'Latest {page_updates}   |   DC PS SENTI time {time_frame}', format='md')

                    # if time_diff_min > 3:
                    #     time_delay_alert.markdown('<span style="color: red">Data delay greater than 2 minutes!</span>',
                    #                               unsafe_allow_html=True)
                    # else:
                    #     time_delay_alert.write("")

                    # remove wrong index
                    complete_df.reset_index(inplace=True)
                    del complete_df['index']

                    complete_df.index = complete_df['OpType']
                    del complete_df['OpType']

                    # complete_df[['Senti_2003', 'Senti_2051', 'Senti_6760', 'Senti_9771']] = complete_df[
                    #     ['Senti_2003', 'Senti_2051', 'Senti_6760', 'Senti_9771']].astype(int)

                    complete_styled_df = style_dataframe_SENTI(complete_df)

                    # update placeholders
                    # summary_placeholder.dataframe(summary_df, width=5000)
                    complete_placeholder_senti.dataframe(complete_styled_df, width=5000)

                    # Sleep for 3 seconds before the next update
                    time.sleep(3)

                except Exception as e:
                    print('Issue:', e)
                    time.sleep(1)
                    pass

        if selected == 'Scenario':
            st.title('SCENARIO')

            # Create placeholders for dynamic content
            time_display_scenario = st.empty()
            time_delay_alert = st.empty()
            # total_dataframe_placeholder = st.empty()
            scenario_placeholder = st.empty()

            while True:
                try:
                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # Read quantity_fetch_time
                    scenario_df = pd.read_csv('Dealer_Data_All_PLdealer_dropcopy.csv')
                    fetch_time = pd.to_datetime(scenario_df['DT'].iloc[-1].split('_')[0])
                    del scenario_df['DT']

                    fetch_time = pd.to_datetime(fetch_time)
                    current_time_dt = pd.to_datetime(current_time)
                    time_diff_min = time_difference_in_minutes(current_time_dt, fetch_time)
                    time_diff_min = abs(time_diff_min)

                    page_updates = datetime.datetime.now().strftime('%S')

                    # Update time_display placeholder
                    time_display_scenario.write(f'Latest {page_updates}   |   SCENARIO Time {fetch_time}', format='md')

                    # if time_diff_min > 3:
                    #     time_delay_alert.markdown('<span style="color: red">Data delay greater than 2 minutes!</span>',
                    #                               unsafe_allow_html=True)
                    # else:
                    #     time_delay_alert.write("")

                    # remove wrong index
                    scenario_df.reset_index(inplace=True)
                    del scenario_df['index']

                    scenario_df.index = scenario_df['Name']
                    del scenario_df['Name']
                    # del scenario_df['Team']

                    # style the data frame
                    scenario_df_styled = style_dataframe_SCENARIO(scenario_df)

                    # update data using place holders
                    scenario_placeholder.dataframe(scenario_df_styled, height=500, width=5000)

                except Exception as e:
                    print('Error:', e)
                    time.sleep(1)
                    pass

                # Sleep for 3 seconds before the next update
                time.sleep(3)


except KeyError:
    # Handle the KeyError when the key is not found in session state
    st.error('User not Logged in')
    st.markdown('<span style="color: blue;">Please go to login in the side menu</span>', unsafe_allow_html=True)

except Exception as e:
    # Handle all other exceptions
    st.error(e)


