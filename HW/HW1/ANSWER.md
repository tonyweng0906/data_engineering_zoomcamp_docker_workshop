# Model 1 HW answer Tonyweng

## Question 1.  What's the version of `pip` in the image?

```bash
pip -V
pip *25.3* from /usr/local/python/3.12.1/lib/python3.12/site-packages/pip (python 3.12)
```

## Question 2. Given the following `docker-compose.yaml`, what is the `hostname` and `port` that pgadmin should use to connect to the postgres database?

*local:postgres*

- db:5432
- **postgres:5432(mistake)**

## Question 3. 
For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a `trip_distance`of less than or equal to 1 mile?
```sql
select 
	count(*) 
from 
	green_trip
where
	"lpep_pickup_datetime" >= '2025-11-01'
	and
	"lpep_pickup_datetime" <= '2025-12-01'
	and
	"trip_distance" <= 1
```
- 8007

## Question 4. Longest trip for each day
```sql
select
	lpep_pickup_datetime as picktime,
	trip_distance
from 
	green_trip
where
	trip_distance <= 100
order by 
	trip_distance desc
limit 1;
```
- 2025-11-14 15:36:27

## Question 5. Biggest pickup zone
Which was the pickup zone with the largest `total_amount` (sum of all trips) on November 18th, 2025?

```sql
select 
	"PULocationID",
	total_sum,
	zpu."Zone"
From
	(select
		sum(total_amount) as total_sum,
		"PULocationID"
	from 
		green_trip
	where 
		Date(lpep_pickup_datetime) = '2025-11-18'
	group by
		"PULocationID"),
	zones as zpu
where
	"PULocationID" = zpu."LocationID"
order by
	total_sum desc
```
- 74, 9281.92, "East Harlem North"

## Question 6. Largest tip
For the passengers picked up in the zone named **"East Harlem North"** in November 2025, which was the drop off zone that had the largest tip?

```sql
SELECT
	sum(tip_amount),
	zdo."Zone" AS "dropoff_loc"
FROM
	green_trip t,
	zones zpu,
	zones zdo
WHERE
	t."PULocationID" = zpu."LocationID" AND
	t."DOLocationID" = zdo."LocationID" AND
	zpu."Zone" = 'East Harlem North' AND
	(t."lpep_pickup_datetime" >= '2025-11-01'
	and
	t."lpep_pickup_datetime" < '2025-12-01')
group by
	zdo."Zone"
order by
	sum(tip_amount) desc
```

```
4242.009999999992	"Upper East Side North"
3425.939999999996	"East Harlem South"
2752.5999999999995	"Upper West Side North"
2403.1700000000023	"Yorkville West"
2121.6499999999987	"Morningside Heights"
```
- East Harlem North(incorrect)
- **Yorkville West(mistake)** not sure the answer



## Question 7. Terraform Workflow
Which of the following sequences, respectively, describes the workflow for:
1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform`

- terraform import, terraform apply -y, terraform destroy
- teraform init, terraform plan -auto-apply, terraform rm
- terraform init, terraform run -auto-approve, terraform destroy
- terraform init, terraform apply -auto-approve, terraform destroy
- terraform import, terraform apply -y, terraform rm

Answers: 
- **terraform init, terraform apply -auto-approve, terraform destroy**

