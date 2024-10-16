const nextConfig = {
  async headers() {
    return [
      {
        source: '/fonts/:font*',
        headers: [
          {
            key: 'Access-Control-Allow-Origin',
            value: '*',
          },
        ],
      },
    ];
  },
};

export default nextConfig;
