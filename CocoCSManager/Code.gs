/**
 * 2026 Coco CS Manager - Apps Script Web App
 * 서버 사이드 코드 (Code.gs)
 */

// 웹앱 진입점 - GET 요청 처리
function doGet(e) {
  const template = HtmlService.createTemplateFromFile('Index');
  
  // URL 파라미터로 페이지 전환 처리 (e가 undefined인 경우 대비)
  template.page = (e && e.parameter && e.parameter.page) ? e.parameter.page : 'main';
  
  return template.evaluate()
    .setTitle('2026 Coco CS Manager')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
}

// HTML 파일 포함 함수 (CSS, JS 분리용)
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}

// ========== 데이터 관련 함수 ==========

/**
 * BS 및 리워크 검색
 * @param {string} searchTerm - 검색어
 * @returns {Array} 검색 결과
 */
function searchBSRework(searchTerm) {
  // TODO: 실제 스프레드시트 연동
  // const ss = SpreadsheetApp.openById('YOUR_SPREADSHEET_ID');
  // const sheet = ss.getSheetByName('BS_리워크');
  
  // 데이터 연동 전까지 빈 배열 반환
  return [];
}

/**
 * AS 실적 데이터 조회
 * @param {Object} filters - 필터 조건
 * @returns {Array} AS 실적 목록
 */
function getASPerformance(filters) {
  // TODO: 실제 스프레드시트 연동
  // 데이터 연동 전까지 빈 배열 반환
  return [];
}

/**
 * CS 통계 데이터 조회
 * @param {string} period - 기간 (daily, weekly, monthly)
 * @returns {Object} 통계 데이터
 */
function getCSStatistics(period) {
  // TODO: 실제 스프레드시트 연동
  return {
    total: 150,
    completed: 120,
    pending: 30,
    rate: 80
  };
}

/**
 * 영업점 주소 검색
 * @param {string} keyword - 검색 키워드
 * @returns {Array} 영업점 목록
 */
function searchBranchAddress(keyword) {
  // TODO: 실제 스프레드시트 연동
  // 데이터 연동 전까지 빈 배열 반환
  return [];
}

/**
 * 배차 목록 조회
 * @returns {Array} 배차 목록
 */
function getDeliveryList(deliveryDate) {
  // TODO: 실제 스프레드시트 연동
  // 데이터 연동 전까지 빈 배열 반환
  return [];
}
