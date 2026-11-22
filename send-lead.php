<?php
// Обработчик формы заявки сайта А-Инжиниринг (хостинг reg.ru).
// Ничего не хранит: принимает заявку и сразу отправляет письмом через почту хостинга.
// Защита: только POST с нашего домена, скрытое поле-ловушка для ботов,
// проверка и обрезка полей, не чаще одной заявки в 30 секунд с одного IP.

// ---- настройки -------------------------------------------------------------
// Куда слать заявки. Когда заведёте ящик на reg.ru — поменяйте на 'info@a-engineering.pro'.
const MAIL_TO   = 'info@engineeringsys.ru';
// От чьего имени уходит письмо: адрес на домене сайта, иначе почтовики считают письмо спамом.
const MAIL_FROM = 'info@a-engineering.pro';
const ALLOWED_HOSTS = ['a-engineering.pro', 'www.a-engineering.pro', 'localhost', '127.0.0.1'];
// ---------------------------------------------------------------------------

header('Content-Type: application/json; charset=utf-8');
header('X-Robots-Tag: noindex');

function reply(int $status, array $body): void {
    http_response_code($status);
    echo json_encode($body, JSON_UNESCAPED_UNICODE);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') reply(405, ['ok' => false, 'error' => 'method']);

$origin = $_SERVER['HTTP_ORIGIN'] ?? ($_SERVER['HTTP_REFERER'] ?? '');
$host = strtolower((string) parse_url($origin, PHP_URL_HOST));
if (!in_array($host, ALLOWED_HOSTS, true)) reply(403, ['ok' => false, 'error' => 'origin']);

$raw = file_get_contents('php://input', false, null, 0, 5001);
if ($raw === false || strlen($raw) > 5000) reply(413, ['ok' => false, 'error' => 'too_large']);
$data = json_decode($raw, true);
if (!is_array($data)) reply(400, ['ok' => false, 'error' => 'bad_json']);

// ловушка: поле скрыто от людей, бот его заполняет — делаем вид, что всё хорошо
if (trim((string) ($data['website'] ?? '')) !== '') reply(200, ['ok' => true]);

function field(array $d, string $k, int $max): string {
    $v = trim(str_replace(["\r", "\0"], '', (string) ($d[$k] ?? '')));
    return mb_substr($v, 0, $max, 'UTF-8');
}
$name    = field($data, 'name', 100);
$phone   = field($data, 'phone', 30);
$message = field($data, 'message', 2000);
$page    = field($data, 'page', 200);
if ($name === '' || strlen(preg_replace('/\D/', '', $phone)) < 10) {
    reply(422, ['ok' => false, 'error' => 'validation']);
}

// не чаще одной заявки в 30 секунд с одного IP (метка во временной папке, без персональных данных)
$ipKey = sys_get_temp_dir() . '/ae_lead_' . sha1(($_SERVER['REMOTE_ADDR'] ?? '') . 'a-engineering');
if (is_file($ipKey) && time() - filemtime($ipKey) < 30) reply(429, ['ok' => false, 'error' => 'too_often']);
@touch($ipKey);

date_default_timezone_set('Europe/Moscow');
$oneLine = fn(string $s) => str_replace("\n", ' ', $s);
$body = "Новая заявка с сайта a-engineering.pro\n\n"
      . "Имя: " . $oneLine($name) . "\n"
      . "Телефон: " . $oneLine($phone) . "\n"
      . "Объект и задача: " . ($message !== '' ? $message : '—') . "\n\n"
      . "Время (МСК): " . date('d.m.Y H:i') . "\n"
      . "Страница: " . ($page !== '' ? $oneLine($page) : '—') . "\n";

$subject = '=?UTF-8?B?' . base64_encode('Заявка с сайта: ' . $oneLine($name)) . '?=';
$headers = implode("\r\n", [
    'From: =?UTF-8?B?' . base64_encode('Сайт А-Инжиниринг') . '?= <' . MAIL_FROM . '>',
    'Reply-To: ' . MAIL_FROM,
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
]);

if (!mail(MAIL_TO, $subject, $body, $headers, '-f' . MAIL_FROM)) {
    reply(502, ['ok' => false, 'error' => 'send_failed']);
}
reply(200, ['ok' => true]);
