document.addEventListener('DOMContentLoaded', function () {

    function updateTimes(val) {
        if (val) {
            const parts = val.split(',');
            if (parts.length === 2) {
                const startInput = document.getElementById('id_start_time');
                const endInput = document.getElementById('id_end_time');
                if (startInput) {
                    startInput.value = parts[0];
                    startInput.dispatchEvent(new Event('change', { bubbles: true }));
                }
                if (endInput) {
                    endInput.value = parts[1];
                    endInput.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }
        }
    }

    document.body.addEventListener('change', function (evt) {
        if (evt.target.id === 'id_slot_selection') {
            updateTimes(evt.target.value);
        }
    });

    document.body.addEventListener('htmx:afterSwap', function (evt) {
        if (evt.target.id === 'id_slot_selection') {
            const startInput = document.getElementById('id_start_time');
            const endInput = document.getElementById('id_end_time');

            if (startInput && endInput && startInput.value && endInput.value) {
                let startVal = startInput.value;
                let endVal = endInput.value;
                if (startVal.length === 5) startVal += ':00';
                if (endVal.length === 5) endVal += ':00';

                const targetValue = startVal + ',' + endVal;

                for (let option of evt.target.options) {
                    if (option.value === targetValue || option.value.startsWith(startVal)) {
                        evt.target.value = option.value;
                        break;
                    }
                }
            }
        }
    });
});
