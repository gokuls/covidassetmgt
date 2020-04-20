from django import template

register = template.Library()
 
@register.filter(name='addclass')
def addclass(field, class_attr):
    return field.as_widget(attrs={'class': class_attr})


@register.filter(name='calculate')
def addclass(total, utilized):
	try:
		c = int(((utilized)/total)*100)
		return c
	except Exception as details:
		return 0


@register.filter(name='change')
def addclass(value):
    try:
    	value = value.split(" ")
    	value = "".join(value)
    	return value
    except:
    	return value

@register.filter(name='addc')
def addclass(total, utilized):
	try:
		mc = int(((utilized)/total)*100)
		print(mc)
	except:
		mc = 0
	if mc < 25:
		return "bg-success"
	elif mc > 25 and mc < 60 :
		return "bg-warning"
	else:
		return "bg-danger"