function getAuthorizationHeaderValue() {
  const username = process.env.USERNAME;
  const password = process.env.PASSWORD;

  if (!username || !password) {
    throw new Error('Missing USERNAME or PASSWORD environment variables');
  }

  return 'Basic ' + Buffer.from(`${username}:${password}`).toString('base64');
}

const ALERT_DEFAULTS = {
    value: 'error',
    column: 'level',
    header: 'Authorization',
    headerValue: getAuthorizationHeaderValue(),
    templateBody: `[{"alert_name":"{alert_name}","org_name":"{org_name}","stream_name":"{stream_name}","alert_type":"{alert_type}","timestamp":"{timestamp}"}]`,
  };
  
  function createAlertTestData(overrides = {}) {
    const suffix = Date.now();
  
    return {
      ...ALERT_DEFAULTS,
      sourceStream: `qa_alert_source_${suffix}`,
      destinationStream: `qa_alert_dest_${suffix}`,
      templateName: `qa_template_${suffix}`,
      destinationName: `qa_destination_${suffix}`,
      alertName: `qa_alert_${suffix}`,
      ...overrides,
    };
  }
  const DASHBOARD_DEFAULTS = {
    logs: [
      { level: 'info', message: 'dashboard record 1', code: '100' },
      { level: 'error', message: 'dashboard record 2', code: '500' },
      { level: 'info', message: 'dashboard record 3', code: '200' },
    ],
  };
  
  function createDashboardTestData(overrides = {}) {
    const suffix = Date.now();
  
    return {
      ...DASHBOARD_DEFAULTS,
      streamName: `qa_dashboard_stream_${suffix}`,
      dashboardName: `qa_dashboard_${suffix}`,
      panelName: `qa_panel_${suffix}`,
      ...overrides,
    };
  }
  
  function createPipelineTestData(overrides = {}) {
    const suffix = Date.now();
  
    return {
      sourceStream: `qa_pipeline_source_${suffix}`,
      destinationStream: `qa_pipeline_dest_${suffix}`,
      pipelineName: `qa_pipeline_${suffix}`,
      streamType: 'logs',
      triggerPayload: [
        { level: 'error', message: 'trigger pipeline routing' },
      ],
      seedPayload: [
        { level: 'info', message: 'seed source stream' },
      ],
      ...overrides,
    };
  }
  
  module.exports = {
    createAlertTestData,
    ALERT_DEFAULTS,
    createDashboardTestData,
    DASHBOARD_DEFAULTS,
    createPipelineTestData,
  };