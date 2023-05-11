import webbrowser
from flask import Flask, render_template, request

app = Flask(__name__)




# 




# Datos de cotización (aluminio y vidrio)
aluminio = {
    'Pulido': 50700,
    'Lacado Brillante': 54200,
    'Anodizado': 57300,
    'Lacado Mate': 53600,
}

vidrio = {
    'Transparente': 8.25,
    'Azul': 5.2,
    'Bronce': 9.15,
    'Esmerilado': 12.75,
}
#Estilo de la ventana
ventana = {
    'O': 1,
    'XO': 2,
    'OXO': 3,
    'OXXO': 4,
}
@app.route('/', methods=['GET', 'POST'])
def cotizacion():
    if request.method == 'POST':
        # Obtener datos de formulario
        estilo = request.form['estilo']
        acabado = request.form['acabado']
        vidrio_tipo = request.form['vidrio']
        esmerilado = request.form.get('Esmerilado', False)
        cantidad = int(request.form['cantidad'])




def calcular_costo_aluminio(acabado):
    return aluminio[acabado]


def calcular_costo_vidrio(vidrio_tipo, esmerilado):
    if vidrio_tipo == 'Bronce':
        costo_vidrio = vidrio['Bronce']
    else:
        costo_vidrio = vidrio[vidrio_tipo]
    
    if esmerilado:
        costo_vidrio = vidrio['Esmerilado']
    
    return costo_vidrio




#Formula de ancho y alto para calcular costo

def calcular_medidas(ancho, alto):
    total_medida_ancho = (ancho - 6) * 2 #ok
    total_medida_alto = (alto - 6) * 2  #ok
    ancho_vidrio = ancho - 3 #ok
    alto_vidrio = alto - 3  #ok
    return total_medida_ancho, total_medida_alto, ancho_vidrio, alto_vidrio



#Sub_total_A para calcular el precio del Aluminio
def calcular_subtotal_aluminio(total_medida_ancho, total_medida_alto, costo_aluminio):
    return (total_medida_ancho + total_medida_alto) * (costo_aluminio / 100)






#Calcular subtotal del ancho del vidrio

def calcular_subtotal_vidrio(ancho_vidrio, alto_vidrio, costo_vidrio):
    total_vidrio = ancho_vidrio * alto_vidrio
    sub_total_vidrio = total_vidrio * costo_vidrio + 5.2
    return total_vidrio, sub_total_vidrio












def calcular_costo_total(acabado, vidrio_tipo, esmerilado, ancho, alto, cantidad, estilo):
    costo_aluminio = calcular_costo_aluminio(acabado)
    costo_vidrio = calcular_costo_vidrio(vidrio_tipo, esmerilado)
    total_medida_ancho, total_medida_alto, ancho_vidrio, alto_vidrio = calcular_medidas(ancho, alto)
    subtotal_aluminio = calcular_subtotal_aluminio(total_medida_ancho, total_medida_alto, costo_aluminio)
    total_vidrio, sub_total_vidrio = calcular_subtotal_vidrio(ancho_vidrio, alto_vidrio, costo_vidrio)
    total_chapas = calcular_total_chapas()
    total_esquinas = calcular_total_esquinas()
    total_ventana = calcular_total_ventana(subtotal_aluminio, sub_total_vidrio, total_chapas, total_esquinas, vidrio_tipo)

    if vidrio_tipo == 'Bronce':
        sub_total_vidrio = total_vidrio * 9.15

    if acabado == 'Lacado Mate' and vidrio_tipo == 'Bronce' and cantidad >= 100:
        descuento = calcular_descuento(total_ventana, cantidad)
        total_ventana -= descuento

    total_ventana = total_ventana * calcular_estilo_ventana(estilo)
    valor_total = total_ventana * cantidad

    total_ventana = total_ventana * estilo_ventana

    # Mostrar resultado
    return render_template('resultado.html', estilo=estilo, acabado=acabado,
                           vidrio_tipo=vidrio_tipo, esmerilado=esmerilado,
                               total=total_ventana,
                               cantidad=cantidad, costo_total=valor_total)
    
    else:
    
    return render_template('formulario.html')
    


if __name__ == '__main__':
    app.run(debug=True)
    # Abre la URL en el navegador predeterminado
    webbrowser.open_new('http://127.0.0.1:5000')
    