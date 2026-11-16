import pandas as pd
import numpy as np
import plotly.express as px

# Generate the Innovative Dataset
np.random.seed(42)
dates = pd.date_range(start="2023-10-01", periods=30)
data = {
    "Date": dates,
    "Sleep_Duration_Hours": np.round(np.random.normal(7, 1.5, 30), 1),
    "Dream_Type": np.random.choice(["Lucid", "Nightmare", "Normal", "None"], 30, p=[0.15, 0.15, 0.5, 0.2]),
    "Morning_Mood_Score": np.random.randint(1, 11, 30),
    "Deep_Sleep_Percentage": np.random.randint(15, 45, 30)
}
df = pd.DataFrame(data)

print("Dataset generated successfully!")
df.head()
fig1 = px.line(df, x="Date", y="Morning_Mood_Score", markers=True,
               title="Morning Mood Over Time",
               template="plotly_dark")

fig1.update_traces(line_color="#00F0FF", marker=dict(size=8))
fig1.update_layout(paper_bgcolor="#0A0A0A", plot_bgcolor="#0A0A0A", font=dict(color="#00F0FF"))
fig1.show()
@interact(mood_category=['All', 'Good Mood (>=7)', 'Bad Mood (<7)'])
def plot_sleep(mood_category):
    if mood_category == 'All':
        filtered_df = df
    elif mood_category == 'Good Mood (>=7)':
        filtered_df = df[df['Morning_Mood_Score'] >= 7]
    else:
        filtered_df = df[df['Morning_Mood_Score'] < 7]
        
    fig3 = px.bar(filtered_df, x="Date", y="Sleep_Duration_Hours",
                  title=f"Sleep Duration ({mood_category})",
                  template="plotly_dark")
    
    fig3.update_traces(marker_color="#8A2BE2")
    fig3.update_layout(paper_bgcolor="#0A0A0A", plot_bgcolor="#0A0A0A", font=dict(color="#00F0FF"))
    fig3.show()
dream_counts = df["Dream_Type"].value_counts().reset_index()
dream_counts.columns = ["Dream_Type", "Count"]

fig2 = px.pie(dream_counts, values="Count", names="Dream_Type", hole=0.4,
              title="Dream Types Distribution",
              template="plotly_dark",
              color_discrete_sequence=["#8A2BE2", "#FF0055", "#00F0FF", "#FFD700"])

fig2.update_layout(paper_bgcolor="#0A0A0A", font=dict(color="#00F0FF"))
fig2.show()
@interact(min_hours=widgets.FloatSlider(min=4, max=10, step=0.5, value=5, description='Min Hours:'))
def plot_violin_mood(min_hours):
    filtered_df = df[df['Sleep_Duration_Hours'] >= min_hours]
    
    if filtered_df.empty:
        print("No data available for this filter.")
        return
        
    fig6 = px.violin(filtered_df, x="Dream_Type", y="Morning_Mood_Score",
                     color="Dream_Type", box=True, points="all",
                     title=f"Mood Distribution by Dream Type (>{min_hours}h sleep)",
                     template="plotly_dark",
                     color_discrete_sequence=["#FF0055", "#00F0FF", "#8A2BE2", "#FFD700"])
    
    fig6.update_layout(paper_bgcolor="#0A0A0A", plot_bgcolor="#0A0A0A", font=dict(color="#00F0FF"))
    fig6.show()
fig3 = px.bar(df, x="Date", y="Sleep_Duration_Hours",
              title="Sleep Duration (Hours)",
              template="plotly_dark")

fig3.update_traces(marker_color="#8A2BE2")
fig3.update_layout(paper_bgcolor="#0A0A0A", plot_bgcolor="#0A0A0A", font=dict(color="#00F0FF"))
fig3.show()
@interact(dream_type=['All'] + list(df['Dream_Type'].unique()))
def plot_scatter_mood_sleep(dream_type):
    if dream_type == 'All':
        filtered_df = df
    else:
        filtered_df = df[df['Dream_Type'] == dream_type]
        
    # Colour is based on 'Morning_Mood_Score' to have different colors
    fig5 = px.scatter(filtered_df, x="Sleep_Duration_Hours", y="Morning_Mood_Score",
                      size="Deep_Sleep_Percentage", 
                      color="Morning_Mood_Score", 
                      hover_data=['Date', 'Dream_Type'],
                      title=f"Sleep Duration vs Morning Mood ({dream_type})",
                      template="plotly_dark",
                      color_continuous_scale=px.colors.sequential.Plasma, # Gradiente vibrante
                      size_max=25)
    
    # Estethicals adjustments for the balls
    fig5.update_traces(marker=dict(line=dict(width=1, color='White')))
    fig5.update_layout(paper_bgcolor="#0A0A0A", plot_bgcolor="#0A0A0A", font=dict(color="#00F0FF"))
    fig5.show()
fig4 = px.box(df, x="Dream_Type", y="Deep_Sleep_Percentage",
              color="Dream_Type",
              title="Deep Sleep % by Dream Type",
              template="plotly_dark",
              color_discrete_sequence=["#8A2BE2", "#FF0055", "#00F0FF", "#FFD700"])

fig4.update_layout(paper_bgcolor="#0A0A0A", plot_bgcolor="#0A0A0A", font=dict(color="#00F0FF"))
fig4.show()
@interact(min_deep_sleep=widgets.IntSlider(min=10, max=40, step=5, value=15, description='Min Deep %:'))
def plot_deep_sleep(min_deep_sleep):
    filtered_df = df[df['Deep_Sleep_Percentage'] >= min_deep_sleep]
    
    if filtered_df.empty:
        print("No data available for this filter.")
        return
        
    fig4 = px.box(filtered_df, x="Dream_Type", y="Deep_Sleep_Percentage",
                  color="Dream_Type",
                  title=f"Deep Sleep % by Dream Type (Min {min_deep_sleep}%)",
                  template="plotly_dark",
                  color_discrete_sequence=["#8A2BE2", "#FF0055", "#00F0FF", "#FFD700"])
    
    fig4.update_layout(paper_bgcolor="#0A0A0A", plot_bgcolor="#0A0A0A", font=dict(color="#00F0FF"))
    fig4.show()