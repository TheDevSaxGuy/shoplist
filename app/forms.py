from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username= StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class ProductForm(FlaskForm):
    description= StringField('Producto', validators=[DataRequired()])
    price= IntegerField('Precio',  validators=[DataRequired()])
    submit = SubmitField('Agregar')

class DeleteProductForm(FlaskForm):
    submit = SubmitField('Borrar')

class TotalCapitalForm(FlaskForm):
    capital = IntegerField('Presupuesto', validators = [DataRequired()])
    submit = SubmitField('Guardar')

class UpdateProductDoneForm(FlaskForm):
    submit = SubmitField('Hecho')