import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from application import app
from flask import render_template, request, redirect, url_for
from wtforms import Form, SelectField, IntegerField, validators


class ProductSelectionForm(Form):
    product_list = pd.read_csv('data/xgb_feature_importances_v1_top500_norm.csv', index_col=0).index
    product_of_interest = SelectField("Product of Interest", [validators.DataRequired()], choices=product_list, )


@app.route('/', methods=["GET", "POST"])
def plot():

    form = ProductSelectionForm(request.form)
    err_msg = ''

    if request.method == "POST":

        if form.validate():
            product_of_interest = request.form["product_of_interest"]
            num_features = int(request.form["num_features"])
            df_fi = pd.read_csv('data/xgb_feature_importances_v1_top500_norm.csv', index_col=0)

            feature_importances = df_fi.loc[product_of_interest]
            feature_importances = feature_importances.sort_values(ascending=False)[:num_features]

            plt.figure(figsize=(12, 6))
            sns.barplot(data=feature_importances.reset_index(), x='index', y=product_of_interest)
            plt.xticks(rotation=90)
            plt.title(f"Feature Importances for {product_of_interest}")
            plt.ylabel('Normalized Feature Importance')
            plt.xlabel('Features')
            plt.savefig('application/static/img.png', format='png', bbox_inches='tight')
            plt.close()

            pass_image = True
            def_num_features = num_features

            return render_template("plot.html", form=form, pass_image=pass_image, err_msg=err_msg, def_num_features=def_num_features)

        else:
            err_msg = 'invalid data input'

    else:
        return render_template("plot.html", form=form, err_msg = err_msg)



def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig
