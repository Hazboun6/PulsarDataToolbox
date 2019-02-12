"""Functions to get the built-in template file"""
import os


__module_dir__ = os.path.dirname(os.path.realpath(__file__))


def get_template(template_name):
    """ Function to get the psrfits template from the templates module dir

       Parameter
       ---------
       template_name: str
           The name of the built-in template.
       Return
       ------
           Full path to the template file. If the request file does not exists,
           it will return None. 
    """
    template_path = os.path.join(__module_dir__, template_name)
    if os.path.exists(template_path):
        return template_path
    else:
        return None
