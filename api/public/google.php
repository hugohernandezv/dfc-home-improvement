<?php
// GET /api/google -> {"rating":4.8,"count":63,"url":"...","reviews":[...]}
// DFC's Google rating, review count and its 5-star reviews (the Places API
// returns at most 5 reviews per place). Google is asked at most once every
// CACHE_TTL seconds; the cached copy is served in between, and the last good
// copy if Google is unreachable. Key: Railway variable GOOGLE_PLACES_KEY.

const PLACE_ID  = 'ChIJZ7xnE0YlaoQRIwPSJ2LbNgc';            // DFC Home Improvement (service-area listing)
const MAPS_URL  = 'https://maps.app.goo.gl/AUjVDsK2nXdHqPy68';
const CACHE     = '/tmp/google-place.json';
const CACHE_TTL = 6 * 3600;

header('Content-Type: application/json');
header('Cache-Control: public, max-age=3600');

function cached() {
    $raw = @file_get_contents(CACHE);
    $data = $raw ? json_decode($raw, true) : null;
    return is_array($data) ? $data : null;
}

function review_out(array $r) {
    $text = $r['originalText']['text'] ?? ($r['text']['text'] ?? '');
    return [
        'author'   => $r['authorAttribution']['displayName'] ?? 'Google user',
        'photo'    => $r['authorAttribution']['photoUri'] ?? '',
        'when'     => $r['relativePublishTimeDescription'] ?? '',
        'time'     => $r['publishTime'] ?? '',
        'rating'   => (int) ($r['rating'] ?? 0),
        'text'     => trim(preg_replace('/[ \t]+/', ' ', $text)),
        'link'     => $r['googleMapsUri'] ?? MAPS_URL,
    ];
}

$data = cached();
$fresh = $data && (time() - ($data['fetched_at'] ?? 0) < CACHE_TTL);

if (!$fresh) {
    $key = getenv('GOOGLE_PLACES_KEY');
    if ($key) {
        $ch = curl_init('https://places.googleapis.com/v1/places/' . PLACE_ID);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT        => 8,
            CURLOPT_HTTPHEADER     => [
                'X-Goog-Api-Key: ' . $key,
                'X-Goog-FieldMask: rating,userRatingCount,reviews',
            ],
        ]);
        $body = curl_exec($ch);
        $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $res  = ($code === 200 && $body) ? json_decode($body, true) : null;
        if (isset($res['rating'], $res['userRatingCount'])) {
            $reviews = array_map('review_out', $res['reviews'] ?? []);
            // Only 5-star reviews with real text; newest first.
            $reviews = array_values(array_filter($reviews, fn($r) => $r['rating'] === 5 && strlen($r['text']) >= 40));
            usort($reviews, fn($a, $b) => strcmp($b['time'], $a['time']));
            $data = [
                'rating'     => round((float) $res['rating'], 1),
                'count'      => (int) $res['userRatingCount'],
                'url'        => MAPS_URL,
                'reviews'    => $reviews,
                'fetched_at' => time(),
            ];
            @file_put_contents(CACHE, json_encode($data), LOCK_EX);
        }
    }
}

if (!$data) {
    http_response_code(503);
    echo '{"error":"google data unavailable"}';
    exit;
}
unset($data['fetched_at']);
echo json_encode($data);
