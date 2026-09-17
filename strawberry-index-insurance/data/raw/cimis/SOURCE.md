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
| `daily_sanity_104_2022.json` | day-precip, metric, station 104 (De Laveaga), 2022 | `d838774a22c40c6fca0e1824b3877d029d1ed8b9df2b7ba7587ddf4f454c0ea4` | 71,179 |
| `daily_sanity_104_2023.json` | day-precip, metric, station 104 (De Laveaga), 2023 | `ef240b2495acd80fdfe97fa42cfe0baffed9679d98faa1829c21c12b8e371467` | 71,191 |

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
    "file": "daily_sanity_104_2022.json",
    "params": {
      "stationNbrs": "104",
      "startDate": "2022-01-01",
      "endDate": "2022-12-31",
      "isHourly": "false",
      "unitOfMeasure": "M",
      "dataItems": "day-precip"
    }
  },
  {
    "file": "daily_sanity_104_2023.json",
    "params": {
      "stationNbrs": "104",
      "startDate": "2023-01-01",
      "endDate": "2023-12-31",
      "isHourly": "false",
      "unitOfMeasure": "M",
      "dataItems": "day-precip"
    }
  }
]
```
