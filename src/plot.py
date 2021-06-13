# import base64
# from io import BytesIO
# from matplotlib.figure import Figure

# def get_plot():
#     # Generate the figure **without using pyplot**.
#     fig = Figure()
#     ax = fig.subplots()
#     ax.plot([1, 2])
#     # Save it to a temporary buffer.
#     buf = BytesIO()
#     fig.savefig(buf, format="png")
#     # Embed the result in the html output.
#     data = base64.b64encode(buf.getbuffer()).decode("ascii")
#     return f"<img src='data:image/png;base64,{data}'/>"


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io
from sklearn.datasets import load_breast_cancer

sns.set()


def get_breast_cancer_df():
    data = load_breast_cancer()
    breast_cancer_df = pd.DataFrame(data['data'])
    breast_cancer_df.columns = data['feature_names']
    breast_cancer_df['target'] = data['target']
    breast_cancer_df['diagnosis'] = [data['target_names'][x] for x in data['target']]
    return breast_cancer_df, data['feature_names']


def _check_columns_in_df(columns_to_check, dataframe):
    """
    Raises value error if a column is found that is not in the dataframe
    :param columns_to_check:
    :param dataframe:
    :return:
    """
    for column in columns_to_check:
        if column not in list(dataframe.columns):
            raise ValueError('Column does not exist in data')


def get_correlation_matrix_as_bytes(data, feature_names):
    """
    Returns a correlation matrix plot as bytes
    :param data:
    :param feature_names: On which features the correlation matrix should be calculated
    :return: io.BytesIO
    """
    corr = data[list(feature_names)].corr(method='pearson')

    f, ax = plt.subplots(figsize=(11, 9))
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})

    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return bytes_image


def get_pair_plot_as_bytes(data, featues_to_consider):
    """

    :param data:
    :param freatures_to_consider: for which features the pairplot should be plotted
    :return: io.BytesIO
    """

    _check_columns_in_df(featues_to_consider, data)

    f, ax = plt.subplots(figsize=(11, 9))
    sns.pairplot(data,
                 x_vars=featues_to_consider,
                 y_vars=featues_to_consider,
                 hue='diagnosis',
                 palette=('Red', '#875FDB'),
                 markers=["o", "D"])

    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return bytes_image

