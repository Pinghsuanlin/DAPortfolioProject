select * from PortfolioProject..covidDeath
order by 3,4

--select * from PortfolioProject..covidVaccinations
--order by 3,4

/*select data that we are using*/
select location, date, population, total_cases, new_cases, total_deaths
from PortfolioProject..covidDeath
order by 1,2

/*looking at total cases and total deaths
show the likelihood of dying if you got covid*/
select location, date, total_cases, total_deaths
, (total_deaths/total_cases)*100 as DeathPercentage
from PortfolioProject..covidDeath
where location like '%taiwan%'
order by 1,2

/*looking at total cases and total deaths
--show what percentage of population got covid*/
select location, date, population, total_cases
, (total_cases/population)*100 as InfectedPercentage
from PortfolioProject..covidDeath
where location like '%taiwan%'
order by 1,2

/*looking at countries with highest infection rate to populations*/
select location, population, max(total_cases) as HighestInfectionCount
, max((total_cases/population)*100) as InfectedPercentage
from PortfolioProject..covidDeath
--where location like '%taiwan%'
group by location, population
order by InfectedPercentage desc

/*showing countries with the highest death count per population*/
select location, max(cast(total_deaths as int)) as HighestDeathCount
--total_deaths is nvarchar(255), we need to convert it into integer
, max((total_deaths/population)*100) as DeathPercentage
from PortfolioProject..covidDeath
--we found there's issue with location, as South Africat, Asia such continent are counted
--so we add condition of continent is not null
where continent is not null
group by location 
order by HighestDeathCount desc

/*break it down by continent*/
select continent, max(cast(total_deaths as int)) as HighestDeathCount
, max((total_deaths/population)*100) as DeathPercentage
from PortfolioProject..covidDeath
where continent is not null
group by continent 
order by HighestDeathCount desc

/*Global numbers (ie. not looking at any location info)
1. How many new cases each day?*/
select date, sum(new_cases) as TotalCases
, sum(cast(new_deaths as int)) as TotalDeaths
, sum(cast(new_deaths as int))/sum(new_cases)*100 as CasesToDeathPercent
from PortfolioProject..covidDeath
where continent is not null
group by date
order by 1,2

--total case, death and percentage
select sum(new_cases) as TotalCases
, sum(cast(new_deaths as int)) as TotalDeaths
, sum(cast(new_deaths as int))/sum(new_cases)*100 as CasesDeathPercent
from PortfolioProject..covidDeath
where continent is not null
--group by date
order by 1,2


--population to vaccinations
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(convert(bigint, vac.new_vaccinations)) OVER (Partition by dea.location order by dea.location, 
dea.date) as RollingPeopleVaccinated--besides cast(int), another way of doing it is convert()
from PortfolioProject..covidDeath as dea
join PortfolioProject..covidVaccinations as vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
order by 2,3

--use CTE
with PopvsVac (Continent, Location, Date, Population, new_vaccinations, RollingPeopleVaccinated)
as 
(
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(convert(bigint, vac.new_vaccinations)) OVER (Partition by dea.location order by dea.location, 
dea.date) as RollingPeopleVaccinated
from PortfolioProject..covidDeath as dea
join PortfolioProject..covidVaccinations as vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
--order by 2,3
)
select *, (RollingPeopleVaccinated/Population)*100 as VacinatedPopulationPercent
from PopvsVac


--Temp Table
drop table if exists #PercentPopulationVaccinated
create table #PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
new_vaccinations numeric,
RollingPeopleVaccinated numeric
)

insert into #PercentPopulationVaccinated

select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(convert(bigint, vac.new_vaccinations)) OVER (Partition by dea.location order by dea.location, 
dea.date) as RollingPeopleVaccinated
from PortfolioProject..covidDeath as dea
join PortfolioProject..covidVaccinations as vac
	on dea.location = vac.location
	and dea.date = vac.date
--where dea.continent is not null

select *, (RollingPeopleVaccinated/Population)*100 as VacinatedPopulationPercent
from #PercentPopulationVaccinated


--create view to store data for future visualization
create view percentPopulationVaccinated as
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(convert(bigint, vac.new_vaccinations)) OVER (Partition by dea.location order by dea.location, 
dea.date) as RollingPeopleVaccinated
from PortfolioProject..covidDeath as dea
join PortfolioProject..covidVaccinations as vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null

select *
from percentPopulationVaccinated
