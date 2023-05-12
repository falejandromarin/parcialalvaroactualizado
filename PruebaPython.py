import webbrowser
import pytest
from flask import Flask, render_template, request

app = Flask(__name__)


#Se establecen los valores en los datos de cotización
aluminio = {
    'Pulido': 50700,
    'Lacado Brillante': 54200,
    'Anodizado': 57300,
    'Lacado Mate': 53600,
    'Otro': 50700

   
}

vidrio = {
    'Transparente': 8.25,
    'Azul': 12.75,
    'Bronce': 9.15,
    'Esmerilado': 12.75,
}


ventana = {
    'O': 1,
    'XO': 2,
    'OXO': 3,
    'OXXO': 4,
}





        # Obtener datos de formulario

        # Resto del código...

#Se reciben los datos enviados por formulario.html
@app.route('/', methods=['GET', 'POST'])
def cotizacion():
    if request.method == 'POST':
        # Obtener datos de formulario
        estilo = request.form['estilo']
        acabado = request.form['acabado']
     
        otroacabado = request.form['otroAcabado']
        vidrio_tipo = request.form['vidrio']
        esmerilado = request.form.get('Esmerilado', False)
        cantidad = int(request.form['cantidad'])




        # Calcular costo de cotización
        costo_aluminio = aluminio[acabado]
        
            
        estilo_ventana = ventana[estilo]
        costo_vidrio = vidrio[vidrio_tipo]
        if vidrio_tipo == 'Bronce':
            costo_vidrio = vidrio['Bronce']
        if esmerilado:
            costo_vidrio = vidrio['Esmerilado']
        


        
        # Calculo de medidas y costos
        ancho = float(request.form['ancho'])
        alto = float(request.form['alto'])
        
        total_medida_ancho = (ancho - 6) * 2
        total_medida_alto = (alto - 6) * 2
        
        #Se inicia total chapas en 16200 y en la linea 92 se aplica la condicion por si la chapa es de bronce
        total_chapas = 16200
        subtotal_aluminio = (total_medida_ancho + total_medida_alto) * (costo_aluminio / 100)
        
        
        #Se establece el total del ancho y alto y se saca el total requerido en el vidrio
        
        ancho_vidrio = ancho - 3
        alto_vidrio = alto - 3
        
        total_vidrio = ancho_vidrio * alto_vidrio
        
        #Se fija la variable del total de las esquinas ya que no es relativa
        total_esquinas = 4 * 4310
        
        
        #Para calcular el costo del vidrio cuando es esmerilado
        if vidrio_tipo == 'Azul':
            if esmerilado:
                sub_total_vidrio = (total_vidrio * 12.75) + 5.2
            else:
                sub_total_vidrio = (total_vidrio * 8.25) + 5.2
        else:
            sub_total_vidrio = total_vidrio * costo_vidrio
 
        
        #Se calcula el costo de las chapas ya que cuado es de tipo bronce varia el precio de la chapa
        total_chapas = 0
        if vidrio_tipo != 'Bronce':
     
            total_chapas = 16200
        else:
            total_chapas = 32400
        
     
     
        #Una vez calculados los sub totales y totales se calcula el total por ventana 
        total_ventana = (subtotal_aluminio + sub_total_vidrio + total_chapas + total_esquinas)*estilo_ventana
        
        
        
        # Se valida si la cantida es mayor a 100 en la refrencia de Bronce y Lacado Mate y asi aplicar el respectivo descuento
        descuento = 0
        if acabado == 'Lacado Mate' and vidrio_tipo == 'Bronce' and cantidad >= 100:
                descuento = (total_ventana * 0.1)*cantidad
      
        
        #Una vez se valida si tiene descuento o no se saca del valor total de la cantidad de ventanas
        valor_total=(total_ventana * cantidad)-descuento

        # Mostrar resultado y enviar parametros a resultado.html
        return render_template('resultado.html', estilo=estilo, acabado=acabado, otroacabado=otroacabado,
                               vidrio_tipo=vidrio_tipo, esmerilado=esmerilado,
                               total=total_ventana,
                               cantidad=cantidad, costo_total=valor_total, descuento=descuento,)
    else:
        # Mostrar formulario
        return render_template('formulario.html')


if __name__ == '__main__':
    app.run(debug=True)
    # Abre la URL en el navegador predeterminado
    webbrowser.open_new('http://127.0.0.1:5000')



