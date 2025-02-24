function showError(message, errorBox) {
    errorBox.classList.add('show'); 
    errorBox.innerHTML = `<span class="error_detail">${message}</span>`;
}
function showErrorSuccess(message, errorBox) {
    errorBox.classList.add('show'); 
    errorBox.innerHTML = `<span class="error_detail success_notify">${message}</span>`;
}


//hien thi the div khi da co cipher hoac plain
function submitForm(event) {
    event.preventDefault();
    var file = document.getElementById("file-cipher");
    const errorBox = document.getElementById('err_cipher');
    errorBox.classList.remove('show'); 
    errorBox.innerHTML = "";
    if (!file) {
        showError("Lỗi: Không tìm thấy input file!", errorBox);
        return;
    }

    if (!file.files || file.files.length === 0) {
        showError("Không có file nào được chọn !", errorBox);
        return;
    }

    const form = event.target;
    const formData = new FormData(form);

    const process = document.getElementById("process");
    process.style.display = "block";

    const dateString = `${new Date().getDate().toString().padStart(2, '0')}/${(new Date().getMonth() + 1).toString().padStart(2, '0')}/${new Date().getFullYear().toString().slice(-2)}`;
    const xhr = new XMLHttpRequest();

    // Thiết lập yêu cầu
    xhr.open('POST', '/cipher', true);

    // Đăng ký trình xử lý sự kiện khi yêu cầu hoàn thành
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            const inp = response.filename_input_1;
            const oup = response.filename_output_1;
            const resultDiv_cha = document.getElementById('add_file_cipher');
            const notify_cipher = document.getElementById('notify_cipher');
            process.style.display = "none";
            resultDiv_cha.innerHTML = 
                '<div class="filename_left"><p>Input: <span>'+ inp +'</span></p><p>Output: <span>'+ oup +'</span></p></div><div class="download_file"><a href="download-cipher" id="download-cipher"><i class="bx bxs-download"></i> Download</a></div>'  
            
            notify_cipher.innerHTML = '<p>Encrypt data success</p><i class="bx bx-check-circle"></i>';
            showErrorSuccess("File encryption successful!", errorBox);
            download_file_cipher(); 
        }
    };
    xhr.open('POST', form.action);
    xhr.send(formData);
    return false;
  }

  function submitForm_2(event) {
    event.preventDefault();
    var file = document.getElementById("file-plain");
    const errorBox = document.getElementById('err_plain');
    errorBox.classList.remove('show'); 
    errorBox.innerHTML = "";
    if (!file) {
        showError("Lỗi: Không tìm thấy input file!", errorBox);
        return;
    }

    if (!file.files || file.files.length === 0) {
        showError("Không có file nào được chọn !", errorBox);
        return;
    }

    const form = event.target;
    const formData = new FormData(form);

    const process_2 = document.getElementById("process_2");
    process_2.style.display = "block";

    const dateString = `${new Date().getDate().toString().padStart(2, '0')}/${(new Date().getMonth() + 1).toString().padStart(2, '0')}/${new Date().getFullYear().toString().slice(-2)}`;
    const xhr = new XMLHttpRequest();

    // Thiết lập yêu cầu
    xhr.open('POST', '/plain', true);

    // Đăng ký trình xử lý sự kiện khi yêu cầu hoàn thành
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            const inp = response.filename_input_2;
            const oup = response.filename_output_2;

            const resultDiv_cha = document.getElementById('add_file_plain');
            const notify_plain = document.getElementById('notify_plain');

            process_2.style.display = "none";
            resultDiv_cha.innerHTML = 
            '<div class="filename_left"><p>Input: <span>'+ inp +'</span></p><p>Output: <span>'+ oup +'</span></p></div><div class="download_file"><a href="download-plain" id="download-plain"><i class="bx bxs-download"></i> Download</a></div>'  
            
            notify_plain.innerHTML = '<p>Decrypt data success</p><i class="bx bx-check-circle"></i>';
            showErrorSuccess("File decryption successfully!", errorBox);
            download_file_plain();
        }
    };
    xhr.open('POST', form.action);
    xhr.send(formData);
    return false;
  }








// tải file khi nhấn download
function download_file_cipher(){
    const downloadButton = document.getElementById('download-cipher');
    downloadButton.addEventListener('click', () => {
        const downloadUrl = '/download-cipher';  
        window.location.href = downloadUrl;
    });    
}

function download_file_plain(){
    const downloadButton2 = document.getElementById('download-plain');
    downloadButton2.addEventListener('click', () => {
        const downloadUrl2 = '/download-plain';  
        window.location.href = downloadUrl2;
    });
}
