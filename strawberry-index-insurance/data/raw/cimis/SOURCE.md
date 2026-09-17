# CIMIS station data — provenance

Publisher: California Department of Water Resources, California Irrigation Management
Information System (CIMIS). Retrieved with the CIMIS Web API.

Retrieved: 2026-09-16
Data endpoint: https://et.water.ca.gov/StationWeb/GetDataByStationNumber
Station endpoint: https://et.water.ca.gov/StationWeb/GetAllStations
Units requested: metric (`unitOfMeasure=M`), so `DayPrecip` is in millimetres.
Data item: `day-precip`.

Authentication: the app key is sent as the `Ocp-Apim-Subscription-Key` HTTP header
(Azure API Management). It never appears in a URL. It is supplied at run time from the
environment or a gitignored file, **is not recorded here and must not be committed.**

The legacy API at `/api/data` was retired after 2026-07-31; requests carrying an
`appKey` query parameter are rejected by the site firewall. See SPEC_CHANGELOG.

Counties filtered: Monterey, San Benito, Santa Clara, Santa Cruz. Station selection for the comparison
is by distance to the analysis units, done in `notebooks/04b_cimis_check.ipynb`.

## Files

| File | Contents | SHA-256 | Bytes |
|---|---|---|---|
| `stations.json` | full CIMIS station list | `89d126189a0b2c89f6d1b4186138d16827fa1d530eee266de5e5955a171a5a28` | 236,681 |
| `daily_event_march.json` | day-precip, metric, stations 3,4,16,19,23,28,37,53,69,89,95,104,111,112,113,114,115,116,126,129,132,143,177,193,209,210,211,214,229,252, 2023-03-09 to 2023-03-14 | `cd15c8763fc475acf38c0f15203db24075055f83772419580145029cbd993985` | 15,245 |
| `daily_context_january.json` | day-precip, metric, stations 3,4,16,19,23,28,37,53,69,89,95,104,111,112,113,114,115,116,126,129,132,143,177,193,209,210,211,214,229,252, 2023-01-04 to 2023-01-16 | `d3aa02b1fab9a114789385c4497a1cc50dd0ca1d284e7d806a0bc46f8767edb3` | 32,834 |
| `daily_annual_2022_00.json` | day-precip, metric, stations 3,4,16,19, calendar 2022 | `523785164afbc94423f9a83bcaebdee795a442ba34f423da4cce89969adfad82` | 94 |
| `daily_annual_2022_01.json` | day-precip, metric, stations 23,28,37,53, calendar 2022 | `523785164afbc94423f9a83bcaebdee795a442ba34f423da4cce89969adfad82` | 94 |
| `daily_annual_2022_02.json` | day-precip, metric, stations 69,89,95,104, calendar 2022 | `d838774a22c40c6fca0e1824b3877d029d1ed8b9df2b7ba7587ddf4f454c0ea4` | 71,179 |
| `daily_annual_2022_03.json` | day-precip, metric, stations 111,112,113,114, calendar 2022 | `77849dfea49beeb0fdc15b1e1660ebce90c75311a1b2fde01ce857b33bd0b376` | 116,689 |
| `daily_annual_2022_04.json` | day-precip, metric, stations 115,116,126,129, calendar 2022 | `19dd0dae64dad5be1bc5ab61bf6e9d20050046f528803630c28d3ff042a1a6ef` | 208,214 |
| `daily_annual_2022_05.json` | day-precip, metric, stations 132,143,177,193, calendar 2022 | `9922da582f46ed708bc7af62708326392008f7435e9c32823e14ba09d6c263ae` | 129,476 |
| `daily_annual_2022_06.json` | day-precip, metric, stations 209,210,211,214, calendar 2022 | `60205d7c1d1a1fbde0bde1227d34c9b54915649be1cf42e7146152a5519f8828` | 274,170 |
| `daily_annual_2022_07.json` | day-precip, metric, stations 229,252, calendar 2022 | `b0d315bb7df25c03c8a5b12ae4e56da396316a23d9b47cc0d6254d048d740fe0` | 124,355 |
| `daily_annual_2023_00.json` | day-precip, metric, stations 3,4,16,19, calendar 2023 | `523785164afbc94423f9a83bcaebdee795a442ba34f423da4cce89969adfad82` | 94 |
| `daily_annual_2023_01.json` | day-precip, metric, stations 23,28,37,53, calendar 2023 | `523785164afbc94423f9a83bcaebdee795a442ba34f423da4cce89969adfad82` | 94 |
| `daily_annual_2023_02.json` | day-precip, metric, stations 69,89,95,104, calendar 2023 | `ef240b2495acd80fdfe97fa42cfe0baffed9679d98faa1829c21c12b8e371467` | 71,191 |
| `daily_annual_2023_03.json` | day-precip, metric, stations 111,112,113,114, calendar 2023 | `18e91d88bd0bb08e3b72efd9d20ccac0df157bdf0d3fd9dd4980d1ed12e9de4e` | 116,696 |
| `daily_annual_2023_04.json` | day-precip, metric, stations 115,116,126,129, calendar 2023 | `1ca194d9322c8f2dd3d00bc18bd2bf1e5780c3d3a5f944db0e674777f3444ee6` | 208,241 |
| `daily_annual_2023_05.json` | day-precip, metric, stations 132,143,177,193, calendar 2023 | `7e2875ca5657e165afdef4329dbff78c45148b17044863828f293cde742e3e79` | 129,482 |
| `daily_annual_2023_06.json` | day-precip, metric, stations 209,210,211,214, calendar 2023 | `2161bdac23a8fde2e037c6f8cb549d42e137d002460570db489d8d5d956b8746` | 274,219 |
| `daily_annual_2023_07.json` | day-precip, metric, stations 229,252, calendar 2023 | `1ff48a1b2a3293e9d7017fe4eebae6e46d33d06edaf76e5a07f5cc59b6a446c3` | 124,370 |

## Request parameters

```json
[
  {
    "file": "stations.json",
    "params": {}
  },
  {
    "file": "daily_event_march.json",
    "params": {
      "stationNbrs": "3,4,16,19,23,28,37,53,69,89,95,104,111,112,113,114,115,116,126,129,132,143,177,193,209,210,211,214,229,252",
      "startDate": "2023-03-09",
      "endDate": "2023-03-14",
      "isHourly": "false",
      "unitOfMeasure": "M",
      "dataItems": "day-precip"
    }
  },
  {
    "file": "daily_context_january.json",
    "params": {
      "stationNbrs": "3,4,16,19,23,28,37,53,69,89,95,104,111,112,113,114,115,116,126,129,132,143,177,193,209,210,211,214,229,252",
      "startDate": "2023-01-04",
      "endDate": "2023-01-16",
      "isHourly": "false",
      "unitOfMeasure": "M",
      "dataItems": "day-precip"
    }
  },
  {
    "file": "daily_annual_2022_00.json",
    "params": {
      "stationNbrs": "3,4,16,19",
      "startDate": "2022-01-01",
      "endDate": "2022-12-31",
      "isHourly": "false",
      "unitOfMeasure": "M",
      "dataItems": "day-precip"
    }
  },
  {
    "file": "daily_annual_2022_01.json",
    "params": {
      "stationNbrs": "23,28,37,53",
      "startDate": "2022-01-01",
      "endDate": "2022-12-31",
      "isHourly": "false",
      "unitOfMeasure": "M",
      "dataItems": "day-precip"
    }
  },
  {
    "file": "daily_annual_2022_02.json",
    "params": {
      "stationNbrs": "69,89,95,104",
      "startDate": "2022-01-01",
      "endDate": "2022-12-31",
      "isHourly": "false",
      "unitOfMeasure": "M",
      "dataItems": "day-precip"
    }
  },
  {
    "file": "daily_annual_2022_03.json",
    "params": {
      "stationNbrs": "111,112,113,114",
      "startDate": "2022-01-01",
      "endDate": "2022-12-31",
      "isHourly": "false",
      "unitOfMeasure": "M",
      "dataItems": "day-precip"
    }
  },
  {
    "file": "daily_annual_2022_04.json",
    "params": {
      "stationNbrs": "115,116,126,129",
      "startDate": "2022-01-01",
      "endDate": "2022-12-31",
      "isHourly": "false",
      "unitOfMeasure": "M",
      "dataItems": "day-precip"
    }
  },
  {
    "file": "daily_annual_2022_05.json",
    "params": {
      "stationNbrs": "132,143,177,193",
      "startDate": "2022-01-01",
      "endDate": "2022-12-31",
      "isHourly": "false",
      "unitOfMeasure": "M",
      "dataItems": "day-precip"
    }
  },
  {
    "file": "daily_annual_2022_06.json",
    "params": {
      "stationNbrs": "209,210,211,214",
      "startDate": "2022-01-01",
      "endDate": "2022-12-31",
      "isHourly": "false",
      "unitOfMeasure": "M",
      "dataItems": "day-precip"
    }
  },
  {
    "file": "daily_annual_2022_07.json",
    "params": {
      "stationNbrs": "229,252",
      "startDate": "2022-01-01",
      "endDate": "2022-12-31",
      "isHourly": "false",
      "unitOfMeasure": "M",
      "dataItems": "day-precip"
    }
  },
  {
    "file": "daily_annual_2023_00.json",
    "params": {
      "stationNbrs": "3,4,16,19",
      "startDate": "2023-01-01",
      "endDate": "2023-12-31",
      "isHourly": "false",
      "unitOfMeasure": "M",
      "dataItems": "day-precip"
    }
  },
  {
    "file": "daily_annual_2023_01.json",
    "params": {
      "stationNbrs": "23,28,37,53",
      "startDate": "2023-01-01",
      "endDate": "2023-12-31",
      "isHourly": "false",
      "unitOfMeasure": "M",
      "dataItems": "day-precip"
    }
  },
  {
    "file": "daily_annual_2023_02.json",
    "params": {
      "stationNbrs": "69,89,95,104",
      "startDate": "2023-01-01",
      "endDate": "2023-12-31",
      "isHourly": "false",
      "unitOfMeasure": "M",
      "dataItems": "day-precip"
    }
  },
  {
    "file": "daily_annual_2023_03.json",
    "params": {
      "stationNbrs": "111,112,113,114",
      "startDate": "2023-01-01",
      "endDate": "2023-12-31",
      "isHourly": "false",
      "unitOfMeasure": "M",
      "dataItems": "day-precip"
    }
  },
  {
    "file": "daily_annual_2023_04.json",
    "params": {
      "stationNbrs": "115,116,126,129",
      "startDate": "2023-01-01",
      "endDate": "2023-12-31",
      "isHourly": "false",
      "unitOfMeasure": "M",
      "dataItems": "day-precip"
    }
  },
  {
    "file": "daily_annual_2023_05.json",
    "params": {
      "stationNbrs": "132,143,177,193",
      "startDate": "2023-01-01",
      "endDate": "2023-12-31",
      "isHourly": "false",
      "unitOfMeasure": "M",
      "dataItems": "day-precip"
    }
  },
  {
    "file": "daily_annual_2023_06.json",
    "params": {
      "stationNbrs": "209,210,211,214",
      "startDate": "2023-01-01",
      "endDate": "2023-12-31",
      "isHourly": "false",
      "unitOfMeasure": "M",
      "dataItems": "day-precip"
    }
  },
  {
    "file": "daily_annual_2023_07.json",
    "params": {
      "stationNbrs": "229,252",
      "startDate": "2023-01-01",
      "endDate": "2023-12-31",
      "isHourly": "false",
      "unitOfMeasure": "M",
      "dataItems": "day-precip"
    }
  }
]
```
