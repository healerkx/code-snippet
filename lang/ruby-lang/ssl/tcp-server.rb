
#
# The crt and key from XAMPP's Apache.
#

require "socket"
require "openssl"
require "thread"

server = TCPServer.new(8080)

ssl_context = OpenSSL::SSL::SSLContext.new
ssl_context.cert = OpenSSL::X509::Certificate.new(File.open("server.crt"))
ssl_context.key = OpenSSL::PKey::RSA.new(File.open("server.key"))

ssl_server = OpenSSL::SSL::SSLServer.new(server, ssl_context)
 
loop do
    connection = server.accept
    Thread.new {
        begin
            while (content = connection.gets)
                content = content.chomp
                $stdout.puts "From Client: #{content}"
                connection.puts "Received #{content}".chomp
                connection.close
            end
        rescue
            $stderr.puts "Error: #{$!}"
        end
    }
end