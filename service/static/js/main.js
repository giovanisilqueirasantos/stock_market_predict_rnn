Vue.component('main-card', {
    props: ['company'],
    template: `
        <div class="xs-12 sm-4 md-3">
            <div v-bind:class="{'main-card': true, 'not-buy': company.color === 0 && !company.loading ? true : false, 'buy': company.color === 1 && !company.loading ? true : false}">
                <span class="name">{{ company.name }}</span>
                <div class="main-info-container">
                    <div v-bind:class="{'loading-container': true, 'show': company.loading}">
                        <div class="spinner">
                            <div class="double-bounce1"></div>
                            <div class="double-bounce2"></div>
                        </div>
                    </div>
                    <div v-if="!company.error" class="info-container">
                        <span class="label">Comprar: <span class="text">{{ company.buy }}</span></span>
                        <span class="label">Vender: <span class="text">{{ company.not_buy }}</span></span>
                    </div>
                    <div v-else class="error-container">
                        <span class="error-message">{{ company.error_message }}</span>
                    </div>
                </div>
            </div>
        </div>
    `
});

const app = new Vue({
    el: '#app',
    data: {
        companies: [
            {name: 'Recrusul On', buy: null, not_but: null, error: false, error_message: '', loading: false, color: null}
        ]
    },
    created() {
        this.recrusul_on_get_data();
    },
    methods: {
        recrusul_on_get_data(){
            this.companies[0].loading = true;
            fetch('http://localhost:8080/recrusul-on').then((resp) => {
                return resp.json();
            }).then((parsed_resp) => {
                if(parsed_resp['ok']){
                    this.companies[0].error = false;
                    this.companies[0].error_message = '';
                    this.companies[0].buy = parsed_resp['prediction'][0];
                    this.companies[0].not_buy = parsed_resp['prediction'][1];
                    if(parsed_resp['prediction'][0] > parsed_resp['prediction'][1]){
                        this.companies[0].color = 1;
                    }else{
                        this.companies[0].color = 0;
                    }
                }else{
                    this.companies[0].error = true;
                    this.companies[0].error_message = parsed_resp.error;
                    this.companies[0].buy = null;
                    this.companies[0].not_buy = null;
                    this.companies[0].color = null;
                }
                this.companies[0].loading = false;
            }).catch((err) => {
                this.companies[0].error = true;
                this.companies[0].error_message = 'Ops, aconteceu algum problema!';
                this.companies[0].buy = null;
                this.companies[0].not_buy = null;
                this.companies[0].loading = false;
                this.companies[0].color = null;
            });
        }
    }
});