import filesize from 'API_/api_one/allure2-master/allure-generator/src/main/javascript/helpers/filesize';

export default function(size) {
    return filesize(size, {base: 2, round: 1});
}
