import seaborn as sns


def corr_plot(df):
    dataplot = sns.heatmap(df.corr(), cmap="YlGnBu", annot=True)
    return dataplot









