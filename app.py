import streamlit as st
import math
import time

st.set_page_config(page_title="Calculadora Multipropósito", layout="wide", page_icon="🧮")

def show_menu():
    st.sidebar.title("Menú")
    options = [
        "Calculadora Científica",
        "Cronómetro",
        "Escala de Diseño",
        "Conversor de Unidades",
        "Calculadora Eléctrica (Ley de Ohm)"
    ]
    choice = st.sidebar.radio("Selecciona una herramienta:", options)
    return choice

def scientific_calculator():
    st.header("Calculadora Científica")
    st.write("Realiza cálculos matemáticos avanzados.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num1 = st.number_input("Número 1", value=0.0)
        num2 = st.number_input("Número 2 (Opcional para algunas operaciones)", value=0.0)
        
    with col2:
        operation = st.selectbox("Operación", [
            "Suma (+)", "Resta (-)", "Multiplicación (*)", "División (/)", 
            "Potencia (x^y)", "Raíz Cuadrada (√x)", "Seno (sin)", "Coseno (cos)", "Tangente (tan)"
        ])
        
    if st.button("Calcular"):
        try:
            if operation == "Suma (+)":
                st.success(f"Resultado: {num1 + num2}")
            elif operation == "Resta (-)":
                st.success(f"Resultado: {num1 - num2}")
            elif operation == "Multiplicación (*)":
                st.success(f"Resultado: {num1 * num2}")
            elif operation == "División (/)":
                if num2 == 0:
                    st.error("Error: División por cero.")
                else:
                    st.success(f"Resultado: {num1 / num2}")
            elif operation == "Potencia (x^y)":
                st.success(f"Resultado: {math.pow(num1, num2)}")
            elif operation == "Raíz Cuadrada (√x)":
                if num1 < 0:
                    st.error("Error: Raíz cuadrada de número negativo.")
                else:
                    st.success(f"Resultado: {math.sqrt(num1)}")
            elif operation == "Seno (sin)":
                st.success(f"Resultado: {math.sin(math.radians(num1))}")
            elif operation == "Coseno (cos)":
                st.success(f"Resultado: {math.cos(math.radians(num1))}")
            elif operation == "Tangente (tan)":
                st.success(f"Resultado: {math.tan(math.radians(num1))}")
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

def stopwatch():
    st.header("Cronómetro")
    st.write("Mide el tiempo de manera sencilla.")
    
    # Manejo del estado del cronómetro
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'elapsed_time' not in st.session_state:
        st.session_state.elapsed_time = 0
    if 'running' not in st.session_state:
        st.session_state.running = False
        
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Iniciar / Reanudar", use_container_width=True):
            if not st.session_state.running:
                st.session_state.start_time = time.time() - st.session_state.elapsed_time
                st.session_state.running = True
                
    with col2:
        if st.button("Pausar", use_container_width=True):
            if st.session_state.running:
                st.session_state.elapsed_time = time.time() - st.session_state.start_time
                st.session_state.running = False
                
    with col3:
        if st.button("Reiniciar", use_container_width=True):
            st.session_state.start_time = None
            st.session_state.elapsed_time = 0
            st.session_state.running = False
            
    # Mostrar el tiempo
    time_placeholder = st.empty()
    
    if st.session_state.running:
        while st.session_state.running:
            current_elapsed = time.time() - st.session_state.start_time
            mins, secs = divmod(current_elapsed, 60)
            hours, mins = divmod(mins, 60)
            time_str = f"{int(hours):02d}:{int(mins):02d}:{secs:05.2f}"
            time_placeholder.markdown(f"<h1 style='text-align: center; color: #4CAF50;'>{time_str}</h1>", unsafe_allow_html=True)
            time.sleep(0.1) # Pausa breve para no saturar la CPU
    else:
        mins, secs = divmod(st.session_state.elapsed_time, 60)
        hours, mins = divmod(mins, 60)
        time_str = f"{int(hours):02d}:{int(mins):02d}:{secs:05.2f}"
        time_placeholder.markdown(f"<h1 style='text-align: center;'>{time_str}</h1>", unsafe_allow_html=True)

def design_scale():
    st.header("Identificador de Escala de Diseño")
    st.write("Determina si tu diseño está en escala de reducción, real o ampliación.")
    
    st.write("Introduce la escala en formato (Dibujo : Objeto Real)")
    col1, col2, col3 = st.columns([1, 0.1, 1])
    
    with col1:
        draw_measure = st.number_input("Medida en el Dibujo", min_value=0.0001, value=1.0, format="%.4f")
    with col2:
        st.markdown("<h3 style='text-align: center; margin-top: 25px;'>:</h3>", unsafe_allow_html=True)
    with col3:
        real_measure = st.number_input("Medida del Objeto Real", min_value=0.0001, value=1.0, format="%.4f")
        
    if st.button("Identificar Escala"):
        ratio = draw_measure / real_measure
        st.write(f"**Relación (Dibujo/Real):** {ratio:.4f}")
        
        if ratio == 1:
            st.success("Escala Natural o Real (1:1). El dibujo tiene el mismo tamaño que el objeto.")
        elif ratio > 1:
            st.info(f"Escala de Ampliación. El dibujo es más grande que el objeto real.")
            st.write(f"Escala simplificada aproximada: **{ratio:.1f} : 1**")
        else:
            st.warning(f"Escala de Reducción. El dibujo es más pequeño que el objeto real.")
            st.write(f"Escala simplificada aproximada: **1 : {1/ratio:.1f}**")

def unit_converter():
    st.header("Conversor de Unidades de Longitud")
    st.write("Convierte entre diferentes unidades de medida.")
    
    # Definir factores de conversión a metros (unidad base)
    conversion_factors = {
        "Milímetros (mm)": 0.001,
        "Centímetros (cm)": 0.01,
        "Metros (m)": 1.0,
        "Kilómetros (km)": 1000.0,
        "Pulgadas (in)": 0.0254,
        "Pies (ft)": 0.3048,
        "Yardas (yd)": 0.9144,
        "Millas (mi)": 1609.34
    }
    
    units = list(conversion_factors.keys())
    
    col1, col2 = st.columns(2)
    
    with col1:
        amount = st.number_input("Cantidad a convertir", value=1.0)
        from_unit = st.selectbox("De:", units, index=units.index("Centímetros (cm)"))
        
    with col2:
        st.write(" ") # Espacio para alinear
        to_unit = st.selectbox("A:", units, index=units.index("Pulgadas (in)"))
        
    if st.button("Convertir"):
        # Convertir de la unidad origen a metros
        amount_in_meters = amount * conversion_factors[from_unit]
        # Convertir de metros a la unidad destino
        result = amount_in_meters / conversion_factors[to_unit]
        
        st.success(f"**{amount}** {from_unit.split(' ')[1]} = **{result:.4f}** {to_unit.split(' ')[1]}")

def electrical_calculator():
    st.header("Calculadora Eléctrica (Ley de Ohm)")
    st.write("Calcula Voltaje (V), Corriente (I) o Resistencia (R).")
    
    st.info("💡 **Ley de Ohm:** V = I × R (El voltaje es igual a la corriente por la resistencia)")
    
    option = st.selectbox("¿Qué deseas calcular?", ["Voltaje (V)", "Corriente (I)", "Resistencia (R)"])
    
    if option == "Voltaje (V)":
        st.write("Para calcular el **Voltaje (V)**, ingresa la Corriente y la Resistencia.")
        col1, col2 = st.columns(2)
        with col1:
            i = st.number_input("Corriente (Amperios - A)", value=0.0, min_value=0.0)
        with col2:
            r = st.number_input("Resistencia (Ohmios - Ω)", value=0.0, min_value=0.0)
        if st.button("Calcular Voltaje"):
            v = i * r
            st.success(f"El Voltaje es: **{v:.2f} Voltios (V)**")
            
    elif option == "Corriente (I)":
        st.write("Para calcular la **Corriente (I)**, ingresa el Voltaje y la Resistencia.")
        col1, col2 = st.columns(2)
        with col1:
            v = st.number_input("Voltaje (Voltios - V)", value=0.0, min_value=0.0)
        with col2:
            r = st.number_input("Resistencia (Ohmios - Ω)", value=1.0, min_value=0.0001) # Evitar división por cero
        if st.button("Calcular Corriente"):
            i = v / r
            st.success(f"La Corriente es: **{i:.4f} Amperios (A)**")
            
    elif option == "Resistencia (R)":
        st.write("Para calcular la **Resistencia (R)**, ingresa el Voltaje y la Corriente.")
        col1, col2 = st.columns(2)
        with col1:
            v = st.number_input("Voltaje (Voltios - V)", value=0.0, min_value=0.0)
        with col2:
            i = st.number_input("Corriente (Amperios - A)", value=1.0, min_value=0.0001) # Evitar división por cero
        if st.button("Calcular Resistencia"):
            r = v / i
            st.success(f"La Resistencia es: **{r:.2f} Ohmios (Ω)**")

def main():
    st.title("🧮 ToolBox: Herramientas y Calculadoras")
    st.markdown("---")
    
    choice = show_menu()
    
    if choice == "Calculadora Científica":
        scientific_calculator()
    elif choice == "Cronómetro":
        stopwatch()
    elif choice == "Escala de Diseño":
        design_scale()
    elif choice == "Conversor de Unidades":
        unit_converter()
    elif choice == "Calculadora Eléctrica (Ley de Ohm)":
        electrical_calculator()

if __name__ == "__main__":
    main()