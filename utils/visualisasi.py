import matplotlib, io, base64
import matplotlib.pyplot as plt

def viz_pie(df):

    sentiment_counts = df['Label'].value_counts()

    matplotlib.use('Agg')
    fig, ax = plt.subplots(figsize=(4, 3))
    fig.patch.set_facecolor('none')
    ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title('Analisis Sentimen')

    # Convert chart to base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.read()).decode()

    return chart_data
