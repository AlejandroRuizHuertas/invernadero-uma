import React, { useState, useEffect } from 'react'

import PageTitle from '../components/Typography/PageTitle'
import SectionTitle from '../components/Typography/SectionTitle'
import {
  Table,
  TableHeader,
  TableCell,
  TableBody,
  TableRow,
  TableFooter,
  TableContainer,
  Badge,
  Avatar,
  Button,
  Pagination,
} from '@windmill/react-ui'
import { EditIcon, TrashIcon } from '../icons'
import { getData } from '../functions/useObtener'
import { useHistory } from 'react-router-dom'


// import response from '../utils/demo/tableData'
// make a copy of the data, for the second table


function Tables() {
  Number.prototype.round = function (places) {
    return +(Math.round(this + "e+" + places) + "e-" + places);
  }

  //DATOS DE INVERNADEROS

  // setup pages control for every table
  const [pageTableInvernaderos, setPageTableInvernaderos] = useState(1)

  // setup data for every table
  const [dataTableInvernaderos, setDataTableInvernaderos] = useState([])
  const [responseInvernaderos, setResponseInvernaderos] = useState([])
  const history = useHistory()

  // pagination setup
  const resultsInvernaderosPerPage = 10
  const totalResultsInvernaderos = responseInvernaderos.length

  // pagination change control
  function onPageChangeTableInvernaderos(p) {
    setPageTableInvernaderos(p)
  }

  // DATOS DE ALERTAS
  // setup pages control for every table
  const [pageTableAnomalias, setPageTableAnomalias] = useState(1)

  // setup data for every table
  const [dataTableAnomalias, setDataTableAnomalias] = useState([])
  const [responseAnomalias, setResponseAnomalias] = useState([])


  // pagination setup
  const resultsAnomaliasPerPage = 10;
  const totalResultsAnomalias = responseAnomalias.length;
 
  const type = {
    ["NOTICE"]: 'neutral',
    ["WARNING"]:'warning',
    ["ERROR"]:'primary',
    ["CRITICAL"]:'danger'
  }

  // pagination change control
  function onPageChangeTableInvernaderos(p) {
    setPageTableInvernaderos(p)
  }
  function onPageChangeTableAnomalias(p) {
    setPageTableAnomalias(p)
  }
  

  //Carga de datos
  useEffect(() => {

    async function cargarDatos() {
      const datosInvernaderos = await getData('/greenhouse/avg_data')
      setResponseInvernaderos(datosInvernaderos.data)
      setDataTableInvernaderos(datosInvernaderos.data)

      const datosAnomalias = await getData('/anomalias');      
      setResponseAnomalias(datosAnomalias.data)
      setDataTableAnomalias(datosAnomalias.data)
    }
    cargarDatos();
  }, [])

  // on page change, load new sliced data
  // here you would make another server request for new data
  useEffect(() => {
    setDataTableInvernaderos(responseInvernaderos.slice((pageTableInvernaderos - 1) * resultsInvernaderosPerPage, pageTableInvernaderos * resultsInvernaderosPerPage))
  }, [pageTableInvernaderos])

  useEffect(() => {
    setDataTableAnomalias(responseAnomalias.slice((pageTableAnomalias - 1) * resultsAnomaliasPerPage, pageTableAnomalias * resultsAnomaliasPerPage))
  }, [pageTableAnomalias])


  return (
    <>
      <PageTitle>Lista de invernaderos</PageTitle>
      <TableContainer className="mb-8">
        <Table>
          <TableHeader>
            <tr>
              <TableCell>Invernadero</TableCell>
              <TableCell>Humedad</TableCell>
              <TableCell>pH del suelo</TableCell>
              <TableCell>Temperatura</TableCell>
              <TableCell>Oxígeno del agua</TableCell>
              <TableCell>pH del agua</TableCell>
              <TableCell>Salinidad</TableCell>
              <TableCell>Acciones</TableCell>
            </tr>
          </TableHeader>
          <TableBody>
            {dataTableInvernaderos.map((invernadero, i) => (
              <TableRow key={i}>
                <TableCell>
                  <div className="flex items-center text-sm">
                    <div>
                      <p className="font-semibold">{invernadero.user.name}</p>

                    </div>
                  </div>
                </TableCell>
                <TableCell>
                  <span className="text-sm">{invernadero.avg_hum.round(2)} %</span>
                </TableCell>
                <TableCell>
                  <span className="text-sm">{invernadero.avg_soil_ph.round(2)}</span>
                </TableCell>
                <TableCell>
                  <span className="text-sm">{invernadero.avg_temp.round(2)} ºC</span>
                </TableCell>
                <TableCell>
                  <span className="text-sm">{invernadero.avg_water_o2.round(2)} mg/l</span>
                </TableCell>
                <TableCell>
                  <span className="text-sm">{invernadero.avg_water_ph.round(2)}</span>
                </TableCell>
                <TableCell>
                  <span className="text-sm">{invernadero.avg_water_salinity.round(2)} mS/cm</span>
                </TableCell>
                <TableCell>
                  <div className="flex items-center space-x-4">
                    <Button layout="link" size="icon" aria-label="Edit" onClick={() => {
                      history.push('/app/greenhouse/' + invernadero.user._id)
                    }}>
                      <EditIcon className="w-5 h-5" aria-hidden="true" />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <TableFooter>
          <Pagination
            totalResults={totalResultsInvernaderos}
            resultsPerPage={resultsInvernaderosPerPage}
            onChange={onPageChangeTableInvernaderos}
            label="Table navigation"
          />
        </TableFooter>
      </TableContainer>

      <PageTitle>Anomalías detectadas</PageTitle>
      <TableContainer className="mb-8">
        <Table>
          <TableHeader>
            <tr>
              <TableCell>IP</TableCell>
              <TableCell>Fecha</TableCell>
              <TableCell>Mensaje</TableCell>
              <TableCell>Tipo</TableCell>
              <TableCell>Usuario</TableCell>
            </tr>
          </TableHeader>
          <TableBody>
            {dataTableAnomalias.map((anomalia, i) => (
              <TableRow key={i}>
                <TableCell>
                  <div className="flex items-center text-sm">
                    <div>
                      <p className="font-semibold">{anomalia.ip}</p>

                    </div>
                  </div>
                </TableCell>
                <TableCell>
                  <span className="text-sm">{new Date(Date.parse(anomalia.date)).toLocaleString('es-ES')}</span>
                </TableCell>
                <TableCell>
                  <span className="text-sm">{anomalia.msg}</span>
                </TableCell>
                <TableCell>
                <Badge type={type[anomalia.type]}>{anomalia.type} </Badge>
                  
                </TableCell>
                <TableCell>
                  <span className="text-sm">{anomalia.user ? anomalia.user.name : ""}</span>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <TableFooter>
          <Pagination
            totalResults={totalResultsAnomalias}
            resultsPerPage={resultsAnomaliasPerPage}
            onChange={onPageChangeTableAnomalias}
            label="Anomaly navigation"
          />
        </TableFooter>
      </TableContainer>
    </>
  )
}

export default Tables
