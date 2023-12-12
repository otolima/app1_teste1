import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title='DASHBOARD DE VENDAS',
    page_icon='💲',
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={
        'Get Help': 'http://www.meusite.com.br',
        'Report a bug': "http://www.meuoutrosite.com.br",
        'About': "Esse app foi desenvolvido no nosso Curso."
    }
)

# Cria o dataframe
df = pd.read_excel(
    io = 'system_extraction.xlsx',
    engine = 'openpyxl',
    sheet_name= 'salesreport',
    usecols='A:J',
    nrows=4400
)

# Cria o sidebar
with st.sidebar:
    logo_teste = Image.open('logo vizion.png')
    st.image(logo_teste, width=300)
    st.subheader('MENU - DASHBOARD DE VENDAS')
    fVendedor = st.selectbox(
        "Selecione o Vendedor:",
        options = df['Vendedor'].unique()
    )
    fProduto = st.selectbox(
        "Selecione o produto:",
        options=df['Produto vendido'].unique()

    )
    fCliente = st.selectbox(
        "Selecione o Cliente:",
        options = df['Cliente'].unique()
    )
# Tabela Qtde vendida por produto
tab1_qtde_produto = df.loc[(
    df['Vendedor'] == fVendedor) &
    (df['Cliente'] == fCliente)
    ]
tab1_qtde_produto = tab1_qtde_produto.drop(columns=['Data'])# esta linha eviata erro no campo Data   
tab1_qtde_produto = tab1_qtde_produto.groupby('Produto vendido').sum().reset_index()

# Tabela de venda e margem
tab2_vendas_margem = df.loc[(
    df['Vendedor'] == fVendedor) &
    (df['Produto vendido'] == fProduto) &
    (df['Cliente'] == fCliente)
]

# Tabela Vendas por Vendedor
tab3_Vendas_vendedor = df.loc[(
    df['Produto vendido'] == fProduto) &
    (df['Cliente'] == fCliente)
]
tab3_Vendas_Vendedor = tab3_Vendas_vendedor.drop(columns=['Data'])
tab3_Vendas_Vendedor = tab3_Vendas_Vendedor.groupby('Vendedor').sum().reset_index()
tab3_Vendas_vendedor = tab3_Vendas_vendedor.drop(columns=['Nº pedido', 'Preço'])

# Venda por Cliente
tab4_Venda_Cliente = df.loc[(
    df['Vendedor'] == fVendedor) &
    (df['Produto vendido'] == fProduto)
    ]
tab4_Venda_Cliente = tab4_Venda_Cliente.drop(columns=['Data'])
tab4_Venda_Cliente = tab4_Venda_Cliente.groupby('Cliente').sum().reset_index()

# Vendas Mensais
tab5_vendas_mensais = df.loc[(
    df['Vendedor'] == fVendedor) &
    (df['Produto vendido'] == fProduto) &
    (df['Cliente'] == fCliente)
]
tab5_vendas_mensais['mm'] = tab5_vendas_mensais['Data'].dt.strftime('%m/%y')

#### Padrões ####
cor_grafico = '#9DD1F1'
altura_grafico=250

# GRÁFICO 1.0 Qtde vendida por produto
graf1_qtde_produto = alt.Chart(tab1_qtde_produto).mark_bar(
    color = cor_grafico,
    cornerRadiusTopLeft=9,
    cornerRadiusTopRight=9,
).encode(
    x = 'Produto vendido',
    y = 'Quantidade',
    tooltip=['Produto vendido','Quantidade']
).properties(height=altura_grafico, title='QUANTIDADE VENDIDA POR PRODUTO'
).configure_axis(grid=False).configure_view(strokeWidth=0)

# GRÁFICO 1.1 valor da venda por produto
graf1_valor_produto = alt.Chart(tab1_qtde_produto).mark_bar(
    color = cor_grafico,
    cornerRadiusTopLeft=9,
    cornerRadiusTopRight=9,
).encode(
    x = 'Produto vendido',
    y = 'Valor Pedido',
    tooltip=['Produto vendido','Valor Pedido']
).properties(height=altura_grafico, title='VALOR TOTAL POR PRODUTO'
).configure_axis(grid=False).configure_view(strokeWidth=0)

#GRAFICO Vendas por Vendedor
graf2_Vendas_Vendedor = alt.Chart(tab3_Vendas_Vendedor).mark_arc(
    innerRadius=100,
    outerRadius=150,    
).encode(
    theta = alt.Theta(field='Valor Pedido', type='quantitative', stack=True),
    color=alt.Color(
        field='Vendedor',
        type='nominal',
        legend=None
    ),
    tooltip=['Vendedor','Valor Pedido'],
    
).properties(height=500, width=560, title='VALOR VENDA POR VENDEDOR')
rot2Ve = graf2_Vendas_Vendedor.mark_text(radius=210, size=14).encode(text='Vendedor')
rot2Vp = graf2_Vendas_Vendedor.mark_text(radius=180, size=12).encode(text='Valor Pedido')


#GRÁFICO Vendadas por Cliente
graf4_vendas_cliente = alt.Chart(tab4_Venda_Cliente).mark_bar(
    color = cor_grafico,
    cornerRadiusTopLeft=9,
    cornerRadiusTopRight=9,
).encode(
    x = 'Cliente',
    y = 'Valor Pedido',
    tooltip=['Cliente','Valor Pedido']
).properties(height=altura_grafico,title='VALOR VENDAS POR CLIENTE'
).configure_axis(grid=False).configure_view(strokeWidth=0)

graf5_vendas_mensais = alt.Chart(tab5_vendas_mensais).mark_line(
    color=cor_grafico,
).encode(
    alt.X('monthdate(Data):T'),
    y = 'Valor Pedido:Q'
).properties(height=altura_grafico, title = 'VENDAS MENSAIS').configure_axis(grid=False
).configure_view(strokeWidth=0)

### PÁGINA PRINCIPAL ###
total_vendas = round(tab2_vendas_margem['Valor Pedido'].sum(),2)
total_margem = round(tab2_vendas_margem['Margem Lucro'].sum(),2)
porc_margem = int(100*total_margem/total_vendas)

st.header(":bar_chart: DASHBOARD DE VENDAS")

dst1, dst2, dst3, dst4 = st.columns([1,1,1,1])
with dst1:
    st.write('**VENDAS TOTAIS:**')
    st.info(f"R$ {total_vendas}")
with dst2:
    st.write('**MARGEM TOTAL:**')
    st.info(f"R$ {total_margem}")

with dst3:
    st.write('**MARGEM %**')
    st.info(f"{porc_margem}%")
st.markdown("---")

### Colunas dos gráficos
col1, col2, col3 = st.columns([1,1,1])
with col1:
    st.altair_chart(graf4_vendas_cliente, use_container_width=True)
    st.altair_chart(graf5_vendas_mensais, use_container_width=True)

with col2:
    st.altair_chart(graf1_qtde_produto, use_container_width=True)
    st.altair_chart(graf1_valor_produto, use_container_width=True)

with col3:
    st.altair_chart(graf2_Vendas_Vendedor+rot2Ve+rot2Vp)

st.markdown('---')


#st.altair_chart(graf1_qtde_produto)
#st.altair_chart(graf1_qtde_produto)
#st.altair_chart(graf2_Vendas_Vendedor)
#st.altair_chart(graf4_vendas_cliente)
#st.altair_chart(graf5_vendas_mensais)
