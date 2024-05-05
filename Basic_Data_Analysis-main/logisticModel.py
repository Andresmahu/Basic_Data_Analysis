import pandas as pd

import logisticModel_CorrelationPlot as cplt

from random import sample

from sklearn.linear_model import LogisticRegression

def run():
    df = pd.read_csv("data/sales.csv")


    df = df.loc[:, ['STATUS', 'TERRITORY2', 'QUANTITYORDERED', 'PRODUCTLINE', 'PRICEEACH', 'MONTH_ID', 'CUSTOMERNAME', 'COUNTRY', 'CONTACTFIRSTNAME', 'CITY']]

    # Corrplot
    #corr_plot_dat = cplt.corr_plot(df.loc[:, ['QUANTITYORDERED', 'PRICEEACH', 'MONTH_ID']])
    #plt.show()

    # Get dummy variables
    df_dum = pd.get_dummies(df)

    # Split data
    status_cancelled_list_false = df_dum.loc[df_dum.loc[:, 'STATUS_Cancelled'] == 0].index.tolist()
    status_cancelled_list_true = df_dum.loc[df_dum.loc[:, 'STATUS_Cancelled'] == 1].index.tolist()

    train_percentage = 0.8
    train_indices_false = sample(status_cancelled_list_false, int(len(status_cancelled_list_false)*train_percentage))
    test_indices_false = list(set(status_cancelled_list_false) - set(train_indices_false))
    train_indices_true = sample(status_cancelled_list_true, int(len(status_cancelled_list_true)*train_percentage))
    test_indices_true = list(set(status_cancelled_list_true) - set(train_indices_true))

    train_indices = train_indices_false + train_indices_true
    test_indices = test_indices_false + test_indices_true


    df_train = df_dum.drop(index=test_indices, axis=0)
    df_test = df_dum.iloc[test_indices, :]

    df_train = df_train.sample(frac=1).reset_index(drop=True)
    df_test = df_test.sample(frac=1).reset_index(drop=True)

    # Get the data with the right format
    X_train = df_train[df_train.columns.difference(['STATUS_Cancelled'])].to_numpy()
    Y_train = df_train.loc[:, ['STATUS_Cancelled']].to_numpy().ravel()
    X_test = df_test[df_test.columns.difference(['STATUS_Cancelled'])].to_numpy()
    Y_test = df_test.loc[:, ['STATUS_Cancelled']].to_numpy().ravel()


    # Building the Logistic model
    logModel = LogisticRegression(solver='lbfgs', max_iter=3000)
    logModel.fit(X_train, Y_train)

    # Testing the model
    print("Logistic Model Score: {}".format(logModel.score(X_test, Y_test)))

    # A perfect score? Apparently, Yes



if __name__ == '__main__':
    run()

