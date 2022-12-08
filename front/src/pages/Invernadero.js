import React, { useEffect, useState } from 'react'

import ChartCard from '../components/Chart/ChartCard'
import { Doughnut, Line, Bar } from 'react-chartjs-2'
import ChartLegend from '../components/Chart/ChartLegend'
import PageTitle from '../components/Typography/PageTitle'
import {
  doughnutOptions,
  lineOptions,
  barOptions,
  doughnutLegends,
  lineLegends,
  barLegends,
} from '../utils/demo/chartsData'
import { useHistory, useParams } from 'react-router-dom'
import { getData, postData } from '../functions/useObtener'
import {

  Button,

} from '@windmill/react-ui'

function Invernadero() {
  const { id } = useParams();
  const history = useHistory();

  const [temp, setTemp] = useState({ labels: [], data: [] })
  const [humedad, setHumedad] = useState({ labels: [], data: [] })
  const [PHSuelo, setPHSuelo] = useState({ labels: [], data: [] })
  const [o2Agua, setO2Agua] = useState({ labels: [], data: [] })
  const [phAgua, setPHAgua] = useState({ labels: [], data: [] })
  const [salAgua, setSalAgua] = useState({ labels: [], data: [] })

  useEffect(() => {

    async function cargarDatos() {
      const datos = await getData(`/greenhouse/${id}/data`);

      setTemp({
        labels: datos.data.map((data) => new Date(data.created).toLocaleString()).slice(0, 20).reverse(),
        data: datos.data.map((data) => data.temp).slice(0, 20).reverse()
      });
      setHumedad({
        labels: datos.data.map((data) => new Date(data.created).toLocaleString()).slice(0, 20).reverse(),
        data: datos.data.map((data) => data.hum).slice(0, 20).reverse()
      });
      setPHSuelo({
        labels: datos.data.map((data) => new Date(data.created).toLocaleString()).slice(0, 20).reverse(),
        data: datos.data.map((data) => data.soil_ph).slice(0, 20).reverse()
      });
      setO2Agua({
        labels: datos.data.map((data) => new Date(data.created).toLocaleString()).slice(0, 20).reverse(),
        data: datos.data.map((data) => data.water_o2).slice(0, 20).reverse()
      })
      setPHAgua({
        labels: datos.data.map((data) => new Date(data.created).toLocaleString()).slice(0, 20).reverse(),
        data: datos.data.map((data) => data.water_ph).slice(0, 20).reverse()
      })
      setSalAgua({
        labels: datos.data.map((data) => new Date(data.created).toLocaleString()).slice(0, 20).reverse(),
        data: datos.data.map((data) => data.water_salinity).slice(0, 20).reverse()
      })

    }
    cargarDatos();
  }, []);

  const handleOpenRiego = () => {
    postData(`/greenhouse/${id}/do_action/irrigation`,{riego:true})
  }

  const handleCloseRiego = () => {
    postData(`/greenhouse/${id}/do_action/irrigation`,{riego:false})
  }

  return (
    <>
      <PageTitle>Gráficas de invernadero</PageTitle>
      <hr></hr>
      <br></br>
      <div className="grid gap-6 mb-8 md:grid-cols-2">

        <ChartCard title="Humedad">
          <Line {...lineOptions(humedad, "Humedad")} />

        </ChartCard>

        <ChartCard title="Temperatura">
          <Line {...lineOptions(temp, "Temperatura")} />

        </ChartCard>

        <ChartCard title="PH en suelo">
          <Line {...lineOptions(PHSuelo, "PH en suelo")} />

        </ChartCard>

        <ChartCard title="Oxígeno en agua">
          <Line {...lineOptions(o2Agua, "Oxígeno en agua")} />

        </ChartCard>

        <ChartCard title="PH en agua">
          <Line {...lineOptions(phAgua, "PH en agua")} />

        </ChartCard>

        <ChartCard title="Salinidad en agua">
          <Line {...lineOptions(salAgua, "Salinidad en agua")} />

        </ChartCard>
        <Button size="large" onClick={() => {
          handleOpenRiego()
        }}>
          Abrir riego
        </Button>
        <Button size="large" onClick={() => {
          handleCloseRiego()
        }}>
          Apagar riego
        </Button>
      </div>
      <hr></hr>
      <br></br>
      <Button size="large" onClick={() => {
        history.push('/app/dashboard')
      }}>
        Volver
      </Button>
      <br></br>
    </>
  )
}

export default Invernadero
