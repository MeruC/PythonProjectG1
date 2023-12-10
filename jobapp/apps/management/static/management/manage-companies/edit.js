window.addEventListener('DOMContentLoaded', function () {
    document.getElementById('logo').addEventListener('change', function () {
        var selectedFile = this.files[0];

        if (selectedFile) {
            var reader = new FileReader();

            reader.onload = function (e) {
                document.getElementById('img_settings').src = e.target.result;
            };

            reader.readAsDataURL(selectedFile);
        }
    });
});