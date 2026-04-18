function getAuthHeader() {
  const username = process.env.USERNAME;
  const password = process.env.PASSWORD;

  if (!username || !password) {
    throw new Error('Missing USERNAME or PASSWORD environment variables');
  }

  return {
    Authorization: 'Basic ' + Buffer.from(`${username}:${password}`).toString('base64'),
  };
}

async function ingestLogs(request, streamName, logs) {
  return request.post(`/api/default/${streamName}/_json`, {
    headers: getAuthHeader(),
    data: logs,
  });
}

async function searchLogs(request, streamName, minutes = 15) {
  const endTime = Date.now() * 1000;
  const startTime = endTime - minutes * 60 * 1000 * 1000;

  return request.post(`/api/default/_search?type=logs`, {
    headers: getAuthHeader(),
    data: {
      query: {
        sql: `SELECT * FROM "${streamName}"`,
        start_time: startTime,
        end_time: endTime,
        from: 0,
        size: 100,
      },
    },
  });
}

module.exports = {
  ingestLogs,
  searchLogs,
};