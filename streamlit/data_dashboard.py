import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_asteroid_csv(file_path):
    """
    Load asteroid data from CSV file and compute future approach indicator.
    """
    df = pd.read_csv(file_path)
    if 'close_approach_date' in df.columns:
        df['close_approach_date'] = pd.to_datetime(df['close_approach_date'], errors='coerce')
        current_time = pd.Timestamp.now()
        df['is_future'] = (df['close_approach_date'] > current_time).astype(bool)
    return df

csv_path = './data/asteroid_close_approaches_2015_2035.csv'

try:
    asteroid_df = load_asteroid_csv(csv_path)
except FileNotFoundError:
    st.error(f'Data file not found at: {csv_path}')
    asteroid_df = pd.DataFrame()

st.title('🌌 Asteroid Core Intelligence Platform')
st.caption("High Resolution Planetary Approach Control Module.")

custom_color_map = {
    True: "#FFC400",
    False: "#929292",
    "True": "#FFC400",
    "False": "#929292",
    "true": "#FFC400",
    "false": "#929292"
}

custom_sequence = ["#00E5FF", "#FF007F", "#7000FF", "#39FF14", "#FFB300"]

if not asteroid_df.empty:
    numeric_cols = asteroid_df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    all_categorical = asteroid_df.select_dtypes(include=['object', 'bool', 'category']).columns.tolist()
    valid_categorical_cols = [
        col for col in all_categorical 
        if asteroid_df[col].nunique() <= 15 and col not in ['designation', 'full_name']
    ]

    st.sidebar.markdown("### 🕹️ Control Center")
    selected_chart = st.sidebar.toggle("🔬 Advanced Scatter View", value=False)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 Global Segmentation")
    
    selected_groupby = st.sidebar.selectbox(
        "Categorical Criteria (Layers/Color):", 
        options=["None"] + valid_categorical_cols,
        index=valid_categorical_cols.index('is_future') + 1 if 'is_future' in valid_categorical_cols else 0
    )
    
    selected_numeric = st.sidebar.selectbox(
        "Control Metric (X Axis):", 
        options=numeric_cols,
        index=numeric_cols.index('dist_lunar') if 'dist_lunar' in numeric_cols else 0
    )

    selected_y_numeric = None
    if selected_chart:
        selected_y_numeric = st.sidebar.selectbox(
            "Secondary Metric (Y Axis):", 
            options=numeric_cols,
            index=numeric_cols.index('absolute_magnitude') if 'absolute_magnitude' in numeric_cols else 0
        )

    if selected_numeric:
        v_series = asteroid_df[selected_numeric].dropna()
        if not v_series.empty:
            num_range = st.sidebar.slider(
                f"Operational Limit: {selected_numeric}", 
                float(v_series.min()), float(v_series.max()), (float(v_series.min()), float(v_series.max()))
            )
            asteroid_df = asteroid_df[
                (asteroid_df[selected_numeric] >= num_range[0]) &
                (asteroid_df[selected_numeric] <= num_range[1])
            ]

    with st.container(border=True):
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.metric(label="☄️ Objects on Radar", value=f"{len(asteroid_df):,}")
        with kpi2:
            avg_dist = asteroid_df['dist_lunar'].mean() if 'dist_lunar' in asteroid_df.columns else 0
            st.metric(label="🌙 Average Proximity", value=f"{avg_dist:.2f} LD", delta="-4.2% vs Historical")
        with kpi3:
            avg_mag = asteroid_df['absolute_magnitude'].mean() if 'absolute_magnitude' in asteroid_df.columns else 0
            st.metric(label="🔆 Absolute Magnitude (H)", value=f"{avg_mag:.1f} H")
        with kpi4:
            futures = asteroid_df['is_future'].sum() if 'is_future' in asteroid_df.columns else 0
            st.metric(label="🚀 Upcoming Alerts", value=f"{futures:,}", delta=f"{futures/len(asteroid_df)*100:.1f}%")

    st.markdown("### 🖥️ Simulation and Visual Analysis Space")

    tab_graphs, tab_analytics, tab_raw_data = st.tabs(["📊 Control Charts", "🔬 Risk Matrix", "🗃️ Data Registry"])

    with tab_graphs:
        col_pie, col_main = st.columns([1, 2])
        color_param = selected_groupby if (selected_groupby and selected_groupby != "None") else None
        
        is_bool_col = selected_groupby == "is_future"
        map_arg = custom_color_map if is_bool_col else None
        seq_arg = None if is_bool_col else custom_sequence

        with col_pie:
            if color_param and len(asteroid_df) > 0:
                fig_pie = px.pie(
                    asteroid_df, 
                    names=color_param, 
                    color=color_param,  
                    hole=0.5,
                    title=f"Distribution: {color_param}", 
                    template="plotly_dark",
                    color_discrete_map=map_arg, 
                    color_discrete_sequence=seq_arg
                )
                fig_pie.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=350)
                st.plotly_chart(fig_pie, use_container_width=True)
                
        with col_main:
            if len(asteroid_df) > 0:
                if not selected_chart:
                    fig_main = px.histogram(
                        asteroid_df, x=selected_numeric, color=color_param, nbins=50,
                        title=f"Operational Frequency: {selected_numeric}", barmode='stack', template="plotly_dark",
                        color_discrete_map=map_arg, color_discrete_sequence=seq_arg
                    )
                else:
                    fig_main = px.scatter(
                        asteroid_df, x=selected_numeric, y=selected_y_numeric, color=color_param,
                        title=f"Orbital Dispersion: {selected_numeric} vs {selected_y_numeric}", template="plotly_dark",
                        color_discrete_map=map_arg, color_discrete_sequence=seq_arg
                    )
                fig_main.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=350)
                selected_data = st.plotly_chart(fig_main, use_container_width=True, on_select="rerun")

    with tab_analytics:
        st.markdown("#### ⚠️ Critical Monitoring Quadrant")
        st.write("Matrix cross-reference for identifying direct space threats based on mass and proximity.")
        
        if 'dist_lunar' in asteroid_df.columns and 'absolute_magnitude' in asteroid_df.columns:
            fig_risk = px.scatter(
                asteroid_df, x='dist_lunar', y='absolute_magnitude', color='is_future',
                color_discrete_map=custom_color_map,
                title="Real Risk Distribution (PHA)", template="plotly_dark"
            )
            fig_risk.add_hline(y=22.0, line_dash="dash", line_color="#FF007F", annotation_text="PHA Size Limit (140m)")
            fig_risk.add_vline(x=19.5, line_dash="dash", line_color="#FFB300", annotation_text="Distance Limit (0.05 au)")
            st.plotly_chart(fig_risk, use_container_width=True)

    display_df = asteroid_df.copy()
    if 'selected_data' in locals() and selected_data and "selection" in selected_data:
        selection_ctx = selected_data["selection"]
        
        selected_category_value = None
        if "points" in selection_ctx and selection_ctx["points"]:
            first_p = selection_ctx["points"][0]
            if "legendgroup" in first_p:
                selected_category_value = first_p["legendgroup"]
                if selected_groupby == "is_future":
                    selected_category_value = selected_category_value in ["true", "True", True]

        if "range" in selection_ctx:
            r_data = selection_ctx["range"]
            if selected_numeric in r_data:
                display_df = display_df[(display_df[selected_numeric] >= float(r_data[selected_numeric][0])) & (display_df[selected_numeric] <= float(r_data[selected_numeric][1]))]
            if selected_chart and selected_y_numeric in r_data:
                display_df = display_df[(display_df[selected_y_numeric] >= float(r_data[selected_y_numeric][0])) & (display_df[selected_y_numeric] <= float(r_data[selected_y_numeric][1]))]
            if selected_groupby != "None" and selected_category_value is not None:
                display_df = display_df[display_df[selected_groupby] == selected_category_value]

        elif "points" in selection_ctx and selection_ctx["points"]:
            points = selection_ctx["points"]
            selected_x_values = [p["x"] for p in points if "x" in p]
            if selected_x_values:
                b_min, b_max = min(selected_x_values), max(selected_x_values)
                if b_min == b_max:
                    delta = float(asteroid_df[selected_numeric].max() - asteroid_df[selected_numeric].min())
                    tolerance = (delta * 0.01) if delta > 0 else 0.001
                    b_min, b_max = b_min - tolerance, b_max + tolerance
                display_df = display_df[(display_df[selected_numeric] >= b_min) & (display_df[selected_numeric] <= b_max)]
                if selected_groupby != "None" and selected_category_value is not None:
                    display_df = display_df[display_df[selected_groupby] == selected_category_value]

    with tab_raw_data:
        st.markdown(f"##### Filtered Data Summary ({len(display_df)} active rows)")
        st.dataframe(
            display_df,
            use_container_width=True,
            column_config={
                "close_approach_date": st.column_config.DatetimeColumn("Approach Date", format="DD/MM/YYYY HH:mm"),
                "dist_lunar": st.column_config.NumberColumn("Lunar Distance", format="%.2f LD"),
                "absolute_magnitude": st.column_config.NumberColumn("Magnitude H", format="%.2f H"),
                "is_future": st.column_config.CheckboxColumn("Is Future?")
            }
        )
else:
    st.warning("Load a valid dataset to structure the dashboard.")