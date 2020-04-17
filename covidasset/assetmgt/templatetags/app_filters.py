from django import template

register = template.Library()
 
@register.filter(name='addclass')
def addclass(field, class_attr):
    return field.as_widget(attrs={'class': class_attr})


@register.filter(name='calculate')
def addclass(total, utilized):
    return int(((utilized)/total)*100)


@register.filter(name='addc')
def addclass(total, utilized):
	mc = int(((utilized)/total)*100)
	if mc < 25:
		return "bg-success"
	elif mc>25 & mc <60:
		return "bg-warning"
	else:
		return "bg-danger"