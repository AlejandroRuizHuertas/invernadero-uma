from form_requests.form_request import FormRequest


class SendGreenHouseDataRequest(FormRequest):

    def rules(self) -> dict:
        return {
            'temp': ['required', 'numeric', 'min:-100', 'max:100'],
            'hum': ['required', 'numeric', 'min:0', 'max:100'],
            'water_ph': ['required', 'numeric', 'min:0', 'max:14'],
            'soil_ph': ['required', 'numeric', 'min:0', 'max:14'],
            'water_salinity': ['required', 'numeric', 'min:0', 'max:5'],
            'water_o2': ['required', 'numeric', 'min:2', 'max:8']
        }