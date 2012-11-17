#!/usr/bin/env ruby



file = File.new("data.txt", "r")
sum = {}
count = {}
while( line = file.gets)
    words = line.split
    if sum.has_key?(words[0])
        sum[words[0]] = sum[words[0]]+words[1].to_i
        count[words[0]]+=1
    else
        sum[words[0]] = words[1].to_i
        count[words[0]]=1
    end

end

new_map = {}

sum.each do |k,v|
    avg = v/count[k]
    puts "#{k} #{avg}"
end
