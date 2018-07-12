from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class Xraylib_Request(FlaskForm):
    comp = StringField(
    'Compound', 
    validators=[DataRequired()]
    )
    
    int_z = StringField(
    'Element', 
    validators=[DataRequired(), 
    NumberRange(min=1, max=118)]
    )
   
    int_z_or_comp = StringField(
    'Element or Compound', 
    validators=[DataRequired()]
    )
       
    float_q = StringField(
    'Momentum Transfer', 
    validators=[DataRequired()]
    )
            
    linetype = StringField(
    'Line Type', 
    validators=[DataRequired()]
    )
    
    shell = StringField(
    'Shell', 
    validators=[DataRequired()]
    )
    
    energy = StringField(
    'Energy', 
    validators=[DataRequired()]
    )
    
    theta = StringField(
    'Theta', 
    validators=[DataRequired()]
    )  
    
    phi = StringField(
    'Phi', 
    validators=[DataRequired()]
    )
    
    density = StringField(
    'Density', 
    validators=[DataRequired()]
    )
    
    pz = StringField(
    'Pz', 
    validators=[DataRequired()]
    )
    
    cktrans = StringField(
    'Cktrans', 
    validators=[DataRequired()]
    )
    
    nistcomp = StringField(
    'Nist Compound', 
    validators=[DataRequired()]
    )
    
    augtrans = StringField(
    'Auger Trans', 
    validators=[DataRequired()]
    )
    
    rad_nuc = StringField(
    'Radio Nuclide', 
    validators=[DataRequired()]
    )
    
    #submit = SubmitField(
    #'Submit',
    #validators=[DataRequired(message="Invalid response")])

#def Function_Request(Flaskform):
    #function = SelectField('Select Function', validators=[DataRequired(message="Invalid response")])
      
# set up function to only run the chosen xraylib method, might work better if it is a form
          
class Request_Error():
        int_z_error = 'Invalid input: please enter an integer.'
        float_q_error = 'Invalid input : please enter an number.'
        error = 'Please enter valid input.'
#then when you need error you do error = request_error.error_name
